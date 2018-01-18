# propyte

# introduction

This is a template Python program and utilities associated.

# setup

```Bash
sudo pip install propyte
```

Set up [Festival](http://www.cstr.ed.ac.uk/projects/festival/), [eSpeak](http://espeak.sourceforge.net/), Pico TTS and [deep_throat](https://github.com/wdbm/deep_throat) for speech capabilities.

```Bash
sudo apt-get -y install \
    festival            \
    espeak              \
    libttspico0         \
    libttspico-utils    \
    libttspico-data
sudo pip install deep_throat
```

Set up Telegram and Telegram messenger CLI for Telegram messaging capabilities.

```Bash
sudo su -
apt-get -y install  \
    libreadline-dev \
    libconfig-dev   \
    libssl-dev      \
    lua5.2          \
    liblua5.2-dev   \
    libevent-dev    \
    libjansson-dev  \
    libpython-dev   \
    make

cd /usr/share
git clone --recursive https://github.com/vysheng/tg.git
cd tg
./configure
make
cd ..
chmod -R 755 tg/
```

Set up Pylint and Graphviz for UML representations

```Bash
sudo apt-get -y install graphviz libgraphviz-dev python-dev
sudo pip install pylint pygraphviz
```

# setup LXPLUS with Pushbullet messaging

Set up a Pushbullet account, create an access token and store a Pushbullet token in the file `~/.pushbullet`. Install Pushbullet on a mobile device.

- [Pushbullet settings](https://www.pushbullet.com/#settings/account)
- [Pushbullet Android](https://play.google.com/store/apps/details?id=com.pushbullet.android)

Miniconda2 is used as an environment. By default, Miniconda is installed at `~/miniconda2` and the Miniconda2 install path is prepended to PATH in `~/.bashrc`.

```Bash
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
chmod 755 Miniconda2-latest-Linux-x86_64.sh
./Miniconda2-latest-Linux-x86_64.sh

export PATH=""${HOME}"/miniconda2/bin:$PATH"
```

```Bash
pip install propyte
```

```Bash
propyte_alert.py --text="hello world"
```

# `propyte_loop_alert_on_new_users.py`

This script loop monitors for new user connections (using `psutil.users()`) and sends an alert (using Pushbullet) is any are detected.

# smuggle

Web modules can be imported using the function `smuggle`. Use this functionality with due regard to security.

```Python
shijian_test = propyte.smuggle(
    URL = "https://raw.githubusercontent.com/wdbm/shijian/master/shijian.py"
)
sys_test = propyte.smuggle(
    module_name = "sys"
)
```

# import_ganzfeld, silence

The context manager function `import_ganzfeld` can be used to import a module such that the module is isolated from command line options and arguments. This can be useful for ROOT.

```Python
with propyte.import_ganzfeld():
    from ROOT import *
```

The context manager function `silence` can be used to silence some code.

# user interactions

There are various functions useful for user interactions: `get_keystroke`, `get_y_or_n`, `get_input`, `get_input_time_limited`, `pause` and `interrogate`.

# commands

The function `engage_command` is available for running Bash commands in the foreground or in the background using subprocess.

# speech

The function `say` is available for generating speech using a number of different speech programs, including Festival, eSpeak, Pico TTS and deep_throat.

# notifications

# Telegram

This module provides Telegram messaging capabilities. It can send and receive Telegram messages. It does this using Telegram, Telegram CLI and pytg.

In order to use Telegram functionality, ensure that both Telegram and Telegram CLI are running. The function `start_messaging_Telegram` attempts to launch Telegram CLI if it does not detect it running.

```bash
/usr/share/tg/bin/telegram-cli     \
    -R                             \
    -W                             \
    -P 4458                        \
    -k /usr/share/tg/tg-server.pub \
    --json                         \
    --permanent-peer-ids           \
    --permanent-peer-ids           \
    --disable-output               \
    --daemonize
```

Messages can be sent in a way like the following:

```Python
import propyte
propyte.start_messaging_Telegram()

propyte.send_message_Telegram(recipient = "@wbreadenmadden", text = "hi")
```

Messages receiving can be engaged in the following way:

```Bash
import propyte
propyte.start_messaging_Telegram()
propyte.start_receiving_messages_Telegram()
```

Messages received can be accessed in a number of ways using various function arguments.

```Python
propyte.get_messages_received_Telegram()
```

```Python
propyte.get_last_message_received_Telegram()
```

```Python
propyte.get_text_last_message_received_Telegram()
```

# Pushbullet

Messages can be sent in ways like the following:

```Python
import propyte
propyte.start_messaging_Pushbullet()

propyte.send_message_Pushbullet(
    recipient = "alice@neutronmail.ch",
    title     = "alert",
    text      = "This is an alert."
)

propyte.send_message_Pushbullet(
    recipients = ["alice@neutronmail.ch"],
    title      = "alert",
    text       = "This is an alert."
)

propyte.send_message_Pushbullet(
    recipient = "alice@neutronmail.ch",
    title     = "price alert",
    filepath  = "prices.png"
)
```

# UML

UML diagrams of a Python project can be generated using Pylint and Graphviz. This can be done by executing the Bash script `UML.sh` in the working directory of the project. This executes the following commands:

```Bash
project_name="${PWD##*/}"
pyreverse -my -A -o png -p ${project_name} **.py
```

This should generate two images, `classes_propyte.png` and `packages_propyte.png`. The classes image is a representation of the classes of the project, their respective data attributes (with types), their respective methods and their inheritances. The packages image is a representation of the module dependencies of the project.
