package util

import (
	"encoding/csv"
	"os"
)

func ReadCsvFile(filename string) ([][]string, error) {
	file, err := os.Open(filename)
	if err != nil {
		Log("Error Loading CSV File", err)
		return [][]string{}, err
	}
	defer file.Close()
	reader := csv.NewReader(file)
	return reader.ReadAll()
}
