alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

alias ll='ls -alF'

alias dev='source /opt/python/cpython/dev/bin/activate'

alias pipup="pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U"
alias rmpy='rm -rf build dist *.spec'
alias rmpyc='find . -name "*.pyc" -exec rm -rf {} \;'

alias json='python -mjson.tool'

export PYTHONSTARTUP=~/.pythonrc
export PYTHONDONTWRITEBYTECODE=True
export PYTHONWARNINGS="ignore:Unverified HTTPS request"

