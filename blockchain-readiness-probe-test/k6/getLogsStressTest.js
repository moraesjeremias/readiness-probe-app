import http from "k6/http";

export const options = {
  vus: 10,
  duration: "1800s",
};

const killerPayload = {
  jsonrpc: "2.0",
  method: "eth_getLogs",
  params: [{ fromBlock: "0xF95C81" }],
  id: 74,
};

const verifierPayload = {
  method: "admin_nodeInfo",
  jsonrpc: "2.0",
  id: "xpto",
};

export default function () {
  const url = `https://nd-${__ENV.NODE_ID}.int.chainstack.com/${__ENV.HASH_KEY}`;
  const payload = JSON.stringify(killerPayload);

  const params = {
    headers: {
      "Content-Type": "application/json",
      "Keep-Alive": "timeout=15, max=100",
    },
  };

  http.post(url, payload, params);
}
