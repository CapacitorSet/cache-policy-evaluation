# Running gem5 on ALPHA

The latest version of gem5 does not work with ALPHA; some tweaks and a specific compiler are required to make it run.

I bundled these tweaks into #[a Docker image](https://github.com/CapacitorSet/gem5-dev) for ease of use; if you want to reproduce them on your own, it's essentially a matter of using gem5 v19.0.0.0 and [a patched version of GCC](http://www.m5sim.org/dist/current/alphaev67-unknown-linux-gnu.tar.bz2).

## Setup

To use the Docker image, first build it:

```sh
git clone https://github.com/CapacitorSet/gem5-dev
docker build -t gem5-dev gem5-dev/docker
```

Then fetch the gem5 sources and build it for ALPHA:

```sh
export GEM5_WORKDIR=/home/user/gem5
docker run --rm -v $GEM5_WORKDIR:/gem5 -it gem5-dev install-source
docker run --rm -v $GEM5_WORKDIR:/gem5 -it gem5-dev build
```

>The build will take several minutes depending on your CPU. As this is a C++ codebase, if you run out of RAM build it manually with fewer cores, eg. replace the "build" step with:

```sh
# on the host
docker run --rm -v $GEM5_WORKDIR:/gem5 -it gem5-dev shell
# in the docker container
scons -j 2 build/ALPHA/gem5.opt
# Here 2 is the number of threads to use for compiling, default=number of CPU cores
```

Finally, you need a specific version of GCC as the MIPS build shipped in the Ubuntu repos doesn't work:

```sh
docker run --rm -v $GEM5_WORKDIR:/gem5 -it gem5-dev install-gcc
```

## Running

Just open a shell into the container and use /gem5/build/ALPHA/gem5.opt as the gem5 binary:

```sh
# on the host
docker run --rm -v $GEM5_WORKDIR:/gem5 -it gem5-dev shell
# in the docker container
/gem5/build/ALPHA/gem5.opt your-script.py
```

>If you plan to run several scripts, it might help to set an alias: `alias gem5=/gem5/build/ALPHA/gem5.opt`.

You'll probably want to clone this repo into GEM5_WORKDIR so that it is accessible from the container:

```sh
# on the host
git clone https://github.com/CapacitorSet/cache-policy-evaluation $GEM5_WORKDIR/project
# in the docker container
alias gem5=/gem5/source/build/ALPHA/gem5.opt
cd /gem5/project

/gem5/build/ALPHA/gem5.opt standalone.py --help
```