package util

import (
	"log"
	"net/http"
	_ "net/http/pprof"
	"os"
	"runtime/pprof"
	"strings"
)

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/plain")
	p := pprof.Lookup("goroutine")
	p.WriteTo(w, 1)
}

func ProfilingMemory(memPort string) {
	if len(memPort) > 0 {
		s := []string{"localhost", ":", memPort}
		h := strings.Join(s, "")
		http.HandleFunc("/", handler)
		go func() {
			log.Println(http.ListenAndServe(h, nil))
		}()
	}
}

func ProfilingCPU(cpuProfile string) {
	if len(cpuProfile) > 0 {
		f, err := os.Create(cpuProfile)
		if err != nil {
			log.Fatal(err)
		}
		pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}
}
