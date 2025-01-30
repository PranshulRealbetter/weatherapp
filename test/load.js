import http from "k6/http";
import { check } from "k6";

export let options = {
  vus: 10,
  duration: "30s",
  // vus: 1,
  // duration: "2s",
};

export default function () {
  const url = "http://localhost:8000/results?query=kolkata";

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  let response = http.get(url, params);

  check(response, {
    "is status 200": (r) => r.status === 200,
  });
}
