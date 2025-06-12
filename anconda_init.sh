
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/powerapps/share/python/anaconda3.53-no-avx/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/powerapps/share/python/anaconda3.53-no-avx/etc/profile.d/conda.sh" ]; then
        . "/powerapps/share/python/anaconda3.53-no-avx/etc/profile.d/conda.sh"
    else
        export PATH="/powerapps/share/python/anaconda3.53-no-avx/bin:$PATH"
    fi
fi

unset __conda_setup
