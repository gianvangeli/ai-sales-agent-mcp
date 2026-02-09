export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Proxy: conserva path + query y redirige a tu backend público (Render)
    const upstream = new URL(env.BACKEND_BASE_URL);
    upstream.pathname = url.pathname;
    upstream.search = url.search;

    const init = {
      method: request.method,
      headers: request.headers,
      body: ["GET", "HEAD"].includes(request.method) ? null : await request.arrayBuffer(),
      redirect: "manual",
    };

    const resp = await fetch(upstream.toString(), init);
    return new Response(resp.body, resp);
  },
};
