package main

import(
	"github.com/sheilkumar/LoadBalancerGo/loadbalancer"
	"github.com/sheilkumar/LoadBalancerGo/server"
	"fmt"
	"net/http"
	"log"
	"time"
	"github.com/gorilla/mux"
// )
)

func main() {
	lb := loadbalancer.LoadBalancer{}
	r := mux.NewRouter()
	// fmt.Println(lb)
	// fmt.Println(sv1)
	lb.AddServer(server.CreateNewServer("server-2", "http://172.21.0.6:5000"))
	lb.AddServer(server.CreateNewServer("server-3", "http://172.21.0.7:5000"))
	lb.AddServer(server.CreateNewServer("server-4", "http://172.21.0.8:5000"))
	lb.AddServer(server.CreateNewServer("server-5", "http://172.21.0.9:5000"))
	fmt.Println(lb)
	r.PathPrefix("/").HandlerFunc(lb.ServeRequest)
	// http.HandleFunc("/", lb.ServeRequest)
	srv := &http.Server{
		Handler: r,
		Addr:    "0.0.0.0:8000",
		// Good practice: enforce timeouts for servers you create!
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}

	log.Fatal(srv.ListenAndServe())
}
