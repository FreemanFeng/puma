package util

import (
	"strings"
	"testing"
)

func TestBase64URLDecode(t *testing.T) {
	data := "lTi7skE3u2lwc6gcgdi9Ew=="
	enc, err := Base64URLDecode(data)
	if err != nil {
		panic("Base64 Decode error!")
	}
	parts := strings.Split(data, "=")
	h := strings.Join(parts, "")
	dec := Base64UrlSafeEncode(enc)
	Log("Old String:", h)
	Log("New String:", dec)
}

//测试AES ECB 加密解密
func TestAoneSignature(t *testing.T) {
	/*
	 *src 要加密的字符串
	 *key 用来加密的密钥 密钥长度可以是128bit、192bit、256bit中的任意一个
	 *16位key对应128bit
	 */
	appName := "uc-feedback-system"
	timestamp := "1512022096668"
	s := []string{"appName=", appName, ";timestamp=", timestamp}
	src := strings.Join(s, "")
	key, _ := Base64URLDecode("RNe1E1p6s474BMRsMIww0g==")

	crypted := AesECBEncrypt(src, string(key))
	AesECBDecrypt(crypted, []byte(key))
}
