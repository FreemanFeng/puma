package util

import (
	"crypto/md5"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"net/url"
	"strings"
)

func Base64Decode(data string) []byte {
	decoded, err := base64.StdEncoding.DecodeString(data)
	if err != nil {
		fmt.Println("decode error:", err)
		return []byte{}
	}
	return decoded
}

func Base64Encode(data []byte) string {
	encoded := base64.StdEncoding.EncodeToString(data)
	return encoded
}

func MD5Sum(data ...string) string {
	s := []string{}
	h := append(s, data...)
	k := strings.Join(h, "")
	Log("raw md5 data:", k)
	b := md5.Sum([]byte(k))
	return hex.EncodeToString(b[:])
}

func SignMapParams(params map[string]string, code string) string {
	keys, data := SortMapString(params)
	Log("keys:", keys)
	path := CombineUrlParamsSorted([]string{}, keys, data)
	Log("path:", path)
	return MD5Sum(path, code)
}

func SignUrlParams(enc_params url.Values, raw_params map[string]string, code string) string {
	params := CombineParams(enc_params, raw_params)
	return SignMapParams(params, code)
}
