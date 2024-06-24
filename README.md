# Delphy paper data

Datasets, scripts for analyzing them, and scripts to generate figures.

Although these scripts were last successfully run in 2024 to prepare, execute and analyze the Delphy and BEAST2 runs,
there is no guarantee that they will run perfectly in the future and/or on your machine.  We do not intend to maintain
these scripts moving forward.  Instead, the aim of this repo is to be living documentation of all the details of the
runs and plots.

## Usage

Create a Python virtualenv and install the associated requirements:
```
python -m venv delphy-env
source ./delphy-env/bin/activate
pip install -r requirements.txt
```

Make symbolic links to the helper binaries you want to use here (you can run `setup_default_links.sh` to look up binaries via `which`, but you'll most likely need to adapt these steps manually):
```
mafft
delphy
treeannotator2 (treeannotator in BEAST2 binaries)
loganalyser2 (loganalyser in BEAST2 binaries)
```

Then enter each of the dataset directory and run the numbered scripts in order.  Warning: the BEAST runs can take a very long time to complete.

In the present repo, all the files created by these runs and analyses have been uploaded.  If you want to regenerate them from scratch, you should delete every *directory* inside each of the dataset directory (e.g., in `sars-cov-2-lemieux`, delete things like `delphy_outputs` and `raw`, but not `00_prepare_runs.py` nor `sample_ids.csv`).

The final plots that were composed into the paper figures are in the `plots` directory of each dataset.


## Software versions used

- Delphy Version 0.99 (build 2020, commit `8e1dda4`)
- BEAST v2.6.2
- BEAGLE commit `3a8d3e6` (Sun Mar 10 2024)


# Preparing the AWS machine for the benchmarks

- Launch an Ubuntu 22.04 LTS x86-64 instance of type `c5a.2xlarge` (8 vCPUs & 16GB memory) with 8GB gp2 storage
- Install BEAST2 (downloaded from BEAST2 releases page: [https://github.com/CompEvol/beast2/releases])
```
  scp -i "~/.ssh/2023-01-29-aws-vs.pem" BEAST.v2.6.2.Linux.tgz ubuntu@ec2-3-78-245-33.eu-central-1.compute.amazonaws.com:.
```
- SSH into the machine, e.g.
```
  ssh -i "~/.ssh/2023-01-29-aws-vs.pem" ubuntu@ec2-3-78-245-33.eu-central-1.compute.amazonaws.com
```
- Upgrade Ubuntu packages
```
    sudo apt update
    sudo apt upgrade  # instance may need to be restarted; do it (`sudo shutdown -r now`) and log back in
```
- Install latest available Java LTS release (17 as of this writing)
```
    sudo apt install openjdk-17-jdk
```
- Check Java works and print version:
```
    java -version

    > openjdk version "17.0.11" 2024-04-16
    > OpenJDK Runtime Environment (build 17.0.11+9-Ubuntu-122.04.1)
    > OpenJDK 64-Bit Server VM (build 17.0.11+9-Ubuntu-122.04.1, mixed mode, sharing)
```
- Unpack BEAST2 
```
    tar -xvzf BEAST.v2.6.2.Linux.tgz
```
- Test it
```
    ./beast/bin/beast -version
    > v2.6.2
```
- Build and install BEAGLE from source (following these instructions: https://github.com/beagle-dev/beagle-lib/wiki/LinuxInstallInstructions)
```
    # Don't download JDK 11, already got JDK 17 above
    sudo apt-get install cmake build-essential autoconf automake libtool git pkg-config # openjdk-11-jdk
    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/  # Need this for CMake to find JDK libs below
    # Also add that same line to ~/.bashrc

    git clone --depth=1 https://github.com/beagle-dev/beagle-lib.git
    cd beagle-lib
    mkdir build
    cd build
    cmake -DBUILD_CUDA=OFF -DBUILD_OPENCL=OFF -DCMAKE_INSTALL_PREFIX:PATH=$HOME ..
    make -j 8 install

    export LD_LIBRARY_PATH=$HOME/lib:$LD_LIBRARY_PATH  # So that BEAST finds BEAGLE
    # Also add that same line to ~/.bashrc
    
    make test  # Should work
    cd ../..  # Back to home
```
- Ensure that BEAST finds BEAGLE
```
    ./beast/bin/beast -beagle_info
    > ...
    > --- BEAGLE RESOURCES ---
    > 
    >0 : CPU (x86_64)
    > Flags: PRECISION_SINGLE PRECISION_DOUBLE COMPUTATION_SYNCH EIGEN_REAL EIGEN_COMPLEX SCALING_MANUAL SCALING_AUTO SCALING_ALWAYS SCALERS_RAW SCALERS_LOG VECTOR_SSE VECTOR_NONE THREADING_NONE PROCESSOR_CPU FRAMEWORK_CPU
```
- Now upload any BEAST2.6.2 XML file and run it with the following command (`-threads -1` uses as many threads as there are CPUs, `-beagle` enforces the use of BEAGLE)
```
    cd path/containing/beast/xml
    time ~/beast/bin/beast -threads -1 -beagle <beast_input.xml>
``` 
