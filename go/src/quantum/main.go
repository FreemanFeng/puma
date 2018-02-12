package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	. "quantum/defs"
	. "quantum/defs/sdk"
	"quantum/report"
	"quantum/sdk"
	"quantum/util"
	"strconv"
)

func Usage() {
	fmt.Fprintln(os.Stderr, "Usage of ", os.Args[0],
		"[-h] -T taskTimeout -R readTimeout -W writeTimeout",
		"[-sdkPort port] [-config config]",
		"[-L logPath] [-P pidPath] [-cpuProfile filePath][-memProfile port]")
	flag.PrintDefaults()
	os.Exit(0)
}

func main() {
	flag.Usage = Usage
	var taskTimeout, readTimeout, writeTimeout, sdkPort int
	var cpuProfile, memPort, config, logPath, pidPath string
	var help bool

	_ = strconv.Atoi
	_ = math.Abs
	flag.Usage = Usage

	// SDK Params
	flag.IntVar(&sdkPort, "sdkPort", SDK_PORT, "Specify SDK Listening Port")

	// Report Params
	flag.StringVar(&config, "config", "", "Specify config file")

	flag.IntVar(&readTimeout, "R", DEFAULT_READ_TIMEOUT, "Specify HTTP Server Read Timeout")
	flag.IntVar(&writeTimeout, "W", DEFAULT_WRITE_TIMEOUT, "Specify HTTP Server Write Timeout")
	flag.IntVar(&taskTimeout, "T", DEFAULT_TASK_TIMEOUT, "Specify Task Timeout")
	flag.StringVar(&cpuProfile, "cpuProfile", "", "write cpu profile to file")
	flag.StringVar(&memPort, "memProfile", "", "port to profile memory")
	flag.StringVar(&logPath, "L", DEFAULT_LOG_PATH, "path for logging files")
	flag.StringVar(&pidPath, "P", DEFAULT_PID_PATH, "path for pids files")

	flag.BoolVar(&help, "h", false, "Show Usage")
	flag.Parse()

	if help {
		Usage()
		return
	}

	util.ProfilingMemory(memPort)
	util.ProfilingCPU(cpuProfile)
	util.SavePID(pidPath, QUANTUM_PID)

	quit := make(chan int)

	go sdk.Run(sdkPort, readTimeout, writeTimeout, quit)

	go report.Run(config, taskTimeout, readTimeout, writeTimeout, quit)

	<-quit
}
