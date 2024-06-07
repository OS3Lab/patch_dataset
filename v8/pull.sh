if command -v gn &> /dev/null; then
    echo " "
else
    if [ ! -d "depot_tools" ]; then
        git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
    fi
    export PATH="$PATH:$(pwd)/depot_tools"
fi
fetch v8
