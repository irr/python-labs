import sys, argparse, paramiko

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--user', 
                        dest="user", 
                        type=str,
                        default="admin",
                        help="user (default: admin)")
parser.add_argument('-p', '--password', 
                        dest="password", 
                        type=str,
                        default=None,
                        help="password")

args, dummy = parser.parse_known_args()

if args.password == None:
    parser.print_help()
    sys.exit(1)

try:
    ssh = paramiko.SSHClient()
    print("creating session as user [%s]..." % (args.user,))
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('127.0.0.1', username=args.user, password=args.password)
    cmd = "uptime"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().strip()
    print(output)
except SSHException as e:
    print("error executing remote command [%s]!" % (cmd,))
    sys.exit(1)
finally:
    ssh.close()
    
print("exiting...")

