package loadbalancer

import(
	"github.com/sheilkumar/LoadBalancerGo/server"
	"net/http"
	"log"
)

type LoadBalancer struct {
	ServerList []*server.Server
}

func (lb *LoadBalancer) AddServer(nextServer *server.Server) {
	lb.ServerList = append(lb.ServerList, nextServer)
}

func (lb *LoadBalancer) EnqueueFront() {
	lb.ServerList = append(lb.ServerList, lb.ServerList[0])
}

func (lb *LoadBalancer) Pop() *server.Server {
	currServer := lb.ServerList[0]
	lb.ServerList = lb.ServerList[1:]
	return currServer
}

func (lb *LoadBalancer) ServeQueueAndRotate() *server.Server {
	lb.EnqueueFront()
	currServer := lb.Pop()
	return currServer
}

func (lb *LoadBalancer) ServeRequest(response http.ResponseWriter, request *http.Request) {
	currServer := lb.ServeQueueAndRotate()
	currServer.ReverseProxy.ServeHTTP(response, request)
	log.Printf("Redirected to %s", currServer.URL)
}

