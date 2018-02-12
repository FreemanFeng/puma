package util

import (
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

func SavePID(pid_path, pid_name string) {
	pid := os.Getpid()
	os.MkdirAll(pid_path, os.ModeDir|os.ModePerm)
	s := []string{pid_path, pid_name}
	h := strings.Join(s, "/")
	s = []string{h, strconv.Itoa(pid)}
	h = strings.Join(s, ".")
	err := ioutil.WriteFile(h, []byte(strconv.Itoa(pid)), 0666)
	if err != nil {
		log.Fatal(err)
	}
}

func InitLogger(log_path, log_name string, ch chan *log.Logger) {
	os.MkdirAll(log_path, os.ModeDir|os.ModePerm)
	s := []string{log_path, log_name}
	h := strings.Join(s, "/")
	logfile, err := os.Create(h)
	defer logfile.Close()
	if err != nil {
		log.Fatal(err)
	}

	mw := io.MultiWriter(os.Stdout, logfile)

	logger := log.New(logfile, "", log.LstdFlags|log.Lmicroseconds|log.Lshortfile)
	logger.SetOutput(mw)
	ch <- logger

	quit := make(chan int)
	// 阻塞直到程序退出
	<-quit
}

func Log(params ...interface{}) {
	fmt.Print(Now(), " ")
	fmt.Println(params...)
}
