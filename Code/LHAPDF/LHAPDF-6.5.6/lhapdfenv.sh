# convenience variables that must exist
prefix=/Users/brageandreastrefjord/Desktop/Github/Master_Thesis/Code/LHAPDF
exec_prefix=${prefix}

export PATH="$exec_prefix/bin":$PATH
export PYTHONPATH="/opt/homebrew/lib/python3.14/site-packages:$PYTHONPATH"
export DYLD_LIBRARY_PATH="${exec_prefix}/lib:$DYLD_LIBRARY_PATH"
export LHAPDF_DATA_PATH="$prefix/share/LHAPDF/"

