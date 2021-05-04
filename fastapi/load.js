// k6 run ./load.js

import http from "k6/http";

export let options = {
    //rps: 100, // maximum number of requests to make per second, in total across all VUs
    //batch: 100, // maximum parallel batch requests that k6 will make per second
    //iterations: 100,
    vus: 10,
    duration: "10s",
    insecureSkipTLSVerify: false,
    noConnectionReuse: false,
    userAgent: "python-fastapi-K6/1.0"
  };

export default function() {
    var params =  { headers: { "Referer": "k6-fastapi/test" } };
    let host = "http://localhost:8000/";
    let response = http.get(`${host}`, params);
}
