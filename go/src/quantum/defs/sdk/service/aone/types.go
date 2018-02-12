package aone

type AoneMessage struct {
	Mobiles string
	Emails  string
	Message string
	Type    string
}

type AoneParams struct {
	ClientId  int
	Signature string
	Nonce     string
}
