package ucstart

type DingMessage struct {
	Mobiles string
	Emails  string
	Message string
	Type    string
}

type DingParams struct {
	ClientId  int
	Signature string
	Nonce     string
}
