package server

import(
	"net/http"
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

func (s *Server) CheckHealth() bool{
	getString := s.URL + "/show-all"
	resp, err := http.Get(getString)
	if err != nil {
		s.Health = false
		return s.Health
	}
	if resp.StatusCode != http.StatusOK {
		s.Health = false
		return s.Health
	}
	s.Health = true
	return s.Health
}