# convenience variables that must exist
prefix=/Users/brageandreastrefjord/Desktop/Github/Master_Thesis/Code/External/LHAPDF/LHAPDF-6.5.6/..
exec_prefix=${prefix}

export PATH="$exec_prefix/bin":$PATH
export PYTHONPATH="/Users/brageandreastrefjord/Desktop/Github/Master_Thesis/Code/External/LHAPDF/LHAPDF-6.5.6/../lib/python3.14/site-packages:$PYTHONPATH"
export DYLD_LIBRARY_PATH="${exec_prefix}/lib:$DYLD_LIBRARY_PATH"
export LHAPDF_DATA_PATH="$prefix/share/LHAPDF/"

