package main

import (
	"fmt"
	"log"
	"net/http"
	"time"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/sheilkumar/LoadBalancerGo/loadbalancer"
	"github.com/sheilkumar/LoadBalancerGo/server"
	// )
)

func main() {
	lb := loadbalancer.LoadBalancer{}
	r := mux.NewRouter()
	// fmt.Println(lb)
	// fmt.Println(sv1)
	lb.AddServer(server.CreateNewServer("server-1","http://api:5000"))
	for i:=2; i<5; i++ {
		lb.AddServer(server.CreateNewServer("server-"+strconv.Itoa(i), "http://api"+strconv.Itoa(i)+":5000"))
	}
	// lb.AddServer(server.CreateNewServer("server-2", "http://api:5000"))
	// lb.AddServer(server.CreateNewServer("server-3", "http://api2:5000"))
	// lb.AddServer(server.CreateNewServer("server-4", "http://api3:5000"))
	// lb.AddServer(server.CreateNewServer("server-5", "http://api4:5000"))
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
	go lb.CheckHealth()
	log.Fatal(srv.ListenAndServe())
}
