package loadbalancer

import(
	"github.com/sheilkumar/LoadBalancerGo/server"
	"net/http"
	"log"
	"github.com/go-co-op/gocron"
	"time"
	"fmt"
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

func (lb *LoadBalancer) ServeHealthyServer() (*server.Server, error) {
	for i:=0; i<len(lb.ServerList); i++ {
		currServer := lb.ServeQueueAndRotate()
		if currServer.Health {
			return currServer, nil
		}
	}
	return nil, fmt.Errorf("No servers available.")
}

func (lb *LoadBalancer) ServeRequest(response http.ResponseWriter, request *http.Request) {
	currServer, err := lb.ServeHealthyServer()
	if err!=nil {
		http.Error(response, err.Error(), http.StatusServiceUnavailable)
	}
	currServer.ReverseProxy.ServeHTTP(response, request)
	log.Printf("Redirected to %s", currServer.URL)
}


func (lb *LoadBalancer) CheckHealth() {
	s := gocron.NewScheduler(time.Local)
	for _, host := range lb.ServerList {
		_, err := s.Every(5).Seconds().Do(func(s *server.Server) {
			healthy := s.CheckHealth()
			if healthy {
				log.Printf("'%s' is Healthy", s.URL)
			} else {
				log.Printf("'%s' is Down", s.URL)
			}
		}, host)
		if err!= nil {
			log.Fatalln(err)
		}
	}
	s.StartAsync()
}