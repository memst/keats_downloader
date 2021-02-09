import sys
import subprocess

from tqdm import tqdm
import ffpb


def execute(argv, name=None, stream=sys.stderr, encoding=None, tqdm=tqdm):
    try:
        with ffpb.ProgressNotifier(file=stream, encoding=encoding, tqdm=tqdm) as notifier:
            notifier.source = name
            cmd = ["ffmpeg"] + argv
            p = subprocess.Popen(cmd, stderr=subprocess.PIPE)

            while True:
                out = p.stderr.read(1).decode("utf-8")
                if out == '' and p.poll() != None:
                    break
                if out != '':
                    #print(out, end="")
                    notifier(out)

    except KeyboardInterrupt:
        print("Exiting.", file=stream)
        return signal.SIGINT + 128  # POSIX standard

    except Exception as err:
        print("Unexpected exception:", err, file=stream)
        return 1

    else:
        if p.returncode != 0:
            print(notifier.lines[-1].decode(notifier.encoding), file=stream)
        return p.returncode
