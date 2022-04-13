package server

import(
	"net/http/httputil"
	"net/url"
)

type Server struct {
	Name         string
	URL          string
	ReverseProxy *httputil.ReverseProxy
	Health       bool
}

func CreateNewServer(name string, urlString string) *Server {
	trueUrl, _ := url.Parse(urlString)
	reverseProxy := httputil.NewSingleHostReverseProxy(trueUrl)
	server := Server{
		Name:         name,
		URL:          urlString,
		ReverseProxy: reverseProxy,
		Health:       true}
	return &server
} 