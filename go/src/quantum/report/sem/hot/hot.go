package hot

import (
	. "quantum/defs/report/sem/hot"
	. "quantum/defs/util"
	"quantum/util"
)

func load_csvdata(source int, file_name string) {
	data, _ := util.ReadCsvFile(file_name)
	for _, k := range data[1:] {
		//util.Log( k)
		if len(k) < 5 || len(k[3]) == 0 {
			continue
		}
		for j := 0; j < 3; j++ {
			if len(k[j]) == 0 {
				k[j] = "通用"
			}
		}
		if len(k[4]) == 0 {
			k[4] = "0"
		}
		util.Log(k)
	}
}

func RunService(done chan int) {
	load_csvdata(SOURCE_SM, CSV_FILE_SEM_TEST)
	done <- SUCCESSFUL
}
