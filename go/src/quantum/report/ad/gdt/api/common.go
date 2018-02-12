package api

import (
	"crypto/md5"
	"encoding/base64"
	"math/rand"
	"net/url"
	. "quantum/defs/report/ad/gdt"
	"strconv"
	"strings"
)

func base64_encode(data []byte) string {
	encoded := base64.StdEncoding.EncodeToString(data)
	return encoded
}

func BuildNonce(task_id int, params url.Values) string {
	account_id := params[PARAM_ACCOUNT_ID][0]
	access_token := params[PARAM_ACCESS_TOKEN][0]
	timestamp := params[PARAM_TIMESTAMP][0]
	s := []string{account_id, access_token, timestamp, strconv.Itoa(task_id), strconv.Itoa(rand.Int())}
	h := strings.Join(s, ",")
	b := md5.Sum([]byte(h))
	return base64_encode(b[:])
}
