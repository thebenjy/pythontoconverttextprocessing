# test_helper.py
import os
import io
import re
import glob
import random
import string
import tempfile
from module_helper import *
from test_helper import *
import module_jobsupport as mjsp
import pathlib
from pathlib import Path
import sys
import shutil
import hashlib
import uuid
import boto3
from botocore.exceptions import ClientError

def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from print statements
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print('Call to %s on line %s of %s from line %s of %s' % \
        (func_name, func_line_no, func_filename,
         caller_line_no, caller_filename))
    return

TURNONDEBUG=False
testdebug_env=os.environ.get("TEST_DEBUG", 'False')
if testdebug_env.lower() == 'true' :
    TURNONDEBUG=True
if testdebug_env.lower() == 'false':
    TURNONDEBUG=False

REGION="us-east-2"
location = {'LocationConstraint': REGION}

# def readfile_to_string(s):
#     txt = Path(s).read_text()
#     print("readfile_to_string: txt: " + txt)
#     return txt

def readfile_to_string(fn):
    s=""
    with open(fn) as f:
        s = f.readlines()
    return s

def readfile_first_line(fn):
    return readfile_to_string(fn)[0] 

def get_env_variable(env_var=None):
    var=""
    # print("checking: env_var: " + env_var)
    if not env_var in os.environ:
        td_print("env_var: " + env_var + " not set", file=sys.stderr)
    else:
        var=os.environ.get(env_var)
    return var

def unset_env_variable(env_var = None):
    try:
        os.environ.pop(env_var)
    except KeyError as ke:
        pass

# call with
#td_print('Setup', self._testMethodName
def td_print(msg, testcase=None):
    tc='generic'
    if not TURNONDEBUG:
        return 
    if testcase != None:
        tc=testcase
    print("Debug : (" + tc + ") " + msg)

# def random_four():
#     """Returns a random 4 charactors"""
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

# we need to rerun each case to make sure stuff not lying around
def gen_tempdir():
    return(tempfile.gettempdir() + FILE_SEPARATOR + mjsp.random_four())

def gen_and_make_tempdir():
    dir=gen_tempdir()
    random_sub_dir=os.path.basename(dir) # we need random sub dir
    td_print('making dir: ' + dir, "gen_and_make_tempdir")
    # os.makedirs(dir)
    path = pathlib.Path(dir)
    ret=path.mkdir(parents=True, exist_ok=True)
    return(dir, random_sub_dir)

def force_delete_bucket(s3resource, bucketname):
    #make sure we dont do something stupid!!
    td_print("s3resource: " + str(s3resource) + ", bucketname: " + str(bucketname))
    if bucketname == "xyzprod":
        sys.exit()
    if bucketname == "xyztrial":
        sys.exit()
    try:
        td_print("bucket: " +  bucketname + ". deleting all objects", 'force_delete_bucket')
        s3resource.Bucket(bucketname).objects.all().delete()
        td_print("deleting bucket: " + bucketname, 'force_delete_bucket')
        s3resource.Bucket(bucketname).delete()
        td_print("successfully deleted : " + bucketname, 'force_delete_bucket')
    except Exception as e:
        td_print("could not delete: " + bucketname + 'error: ' + str(e), 'force_delete_bucket')
        pass

def delete_and_create_bucket(s3resource,bucketname):
    force_delete_bucket(s3resource, bucketname)
    try:
        td_print("creating bucket: " + bucketname, 'delete_and_create_bucket')
        ret=s3resource.create_bucket(Bucket=bucketname, CreateBucketConfiguration=location)
    except Exception as e:
        td_print("delete_and_create_bucket: Bucket create Error: " + str(e))
        return False
        # do nothing
        dumpvar=""
    return True

#https://stackoverflow.com/questions/3397752/copy-multiple-files-in-python
def recursive_copy_files(source_path, destination_path, override=False):
    """
    Recursive copies files from source  to destination directory.
    :param source_path: source directory
    :param destination_path: destination directory
    :param override if True all files will be overridden otherwise skip if file exist
    :return: count of copied files
    """
    td_print('source: ' + source_path + ", destination_path: " + destination_path, "recursive_copy_files")
    files_count = 0
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
    items = glob.glob(source_path + '/*')
    for item in items:
        td_print('item: ' + item, "recursive_copy_files")
        if os.path.isdir(item):
            path = os.path.join(destination_path, item.split('/')[-1])
            files_count += recursive_copy_files(source_path=item, destination_path=path, override=override)
        else:
            file = os.path.join(destination_path, item.split('/')[-1])
            if not os.path.exists(file) or override:
                td_print('copying file: from: ' + item + ', to: ' + file, "recursive_copy_files")
                shutil.copyfile(item, file)
                files_count += 1
    return files_count

# downloaded files go into tmp dir / timestamp
# note when we specify xxxx/2018 to copy, it doesn't copy the base dir 2018
def setup_predownloaded_files_test(inputfiledir, timestamp):
    tmp_dir, randompart=gen_and_make_tempdir()
    basedir=os.path.basename(inputfiledir)

    # now make the processed_tar_dir (now tweets_processed)
    os.makedirs(tmp_dir + FILE_SEPARATOR + 'tweets_processed', exist_ok=True)

    new_dir=tmp_dir + FILE_SEPARATOR + timestamp + FILE_SEPARATOR + basedir
    td_print('making dir: ' + new_dir, "setup_predownloaded_files_test")
    # os.makedirs(dir)
    # path = pathlib.Path(new_dir)
    # path.parent.mkdir(parents=True, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)

     # copy over the file list 
    recursive_copy_files(inputfiledir, new_dir)

    return tmp_dir


# returns the full tmp dir created
# random sub dir that forms the temp path
def setup_filetest(s3r,buck,subdir=""):
    delete_and_create_bucket(s3r, buck)
    tmp_dir, random_sub_dir=gen_and_make_tempdir()
    # os.makedirs(tmp_dir)
    # final_tmp_dir=tmp_dir + FILE_SEPARATOR + subdir
    final_tmp_dir=tmp_dir 
    td_print("setup tmpdir: " + final_tmp_dir + ", the random str part: " + random_sub_dir, "setup_filetest")
    return final_tmp_dir, random_sub_dir


# takes a file list of download archive org files
# and extracts the content to match the incoming mock file list
# e.g. remove base sub / temp directories and empty directories
def generate_matching_filelist_archorgfiles(filelist, yeardir,downloadsubdir=""):
    newlist=[]
    for f in filelist:
        replaced = re.sub('^/.*'+yeardir, "/"+yeardir, f)
        newlist.append(replaced)
    op=[re.findall("(\/.*json.bz2)", i) for i in re.split(",", str(newlist))]
    newop=[]
    for o in op:
        newop.append(str(o).replace("'", "").replace("[", "").replace("]", ""))
    newnewop=[]
    for n in newop:
        if n != '':
            newnewop.append(n.lstrip('/'))
    return newnewop

def upload_s3_data_files(s3resource, bucketname, filelist, testfilesdir, newoffsetdir=None):
    td_print("upload_s3_data_files incoming: " + str(filelist) + ", bucketname: " + bucketname)
    offset_dir=""
    if newoffsetdir != None:
        offset_dir = newoffsetdir
        offset_dir=mjsp.normalise_path(offset_dir) + "/"

    for f in filelist:
        td_print("upload_s3_data_files: object put : " + testfilesdir + f )
        ret=s3resource.Object(bucketname, offset_dir + f).put(Body=open(testfilesdir + f, 'rb'))
        td_print("upload_s3_data_files: PUT ok: " + testfilesdir + f + "\nto: " + offset_dir + f + ", ret:" + str(ret), "upload_s3_data_files")

def check_s3_data_file_uploaded(s3resource, bucketname, s3file):
    try:
        s3resource.Object(bucketname, s3file).load()
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            # The object does not exist.
            return False
        else:
            # Something else has gone wrong.
            raise
    else:
        return True

def compare_files_equal(f1,f2):
    return(list(io.open(f1))==list(io.open(f2)))

def compare_files_equal_usingdiff(f1,f2):
    s="diff -u --strip-trailing-cr " +  f1 + " " + f2
    ret=os.system(s)
    return ret==0


# return true if same
def compare_binary_files_equal(f1,f2):
    s="cmp " + " " + f1 + " " + f2
    ret=os.system(s)
    return ret==0

def hash_md5(filename):
    md5_hash = hashlib.md5()
    a_file = open(filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return digest

def generate_tempfile():
    f = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
    f = open(f.name, 'w')
    f.write("temp text")
    f.close
    return f.name

def list_s3folder(s3resource, bucketName):
    file_list=[]
    bucket = s3resource.Bucket(bucketName) 
    for obj in bucket.objects.all():
        file_list.append(obj.key)
    return file_list

# https://stackoverflow.com/questions/63116813/check-whether-a-json-object-is-a-part-of-another-json-object
def is_subset(a,b):
    def recursive_check_subset(a,b):
        for x in a:
            if not isinstance(a[x],dict):
                yield (x in b ) and (a[x] == b[x]) #return a bool
            else:
                if x in b:
                    yield all(recursive_check_subset(a[x],b[x]))
                else:
                    yield False
    return all(recursive_check_subset(a,b))

