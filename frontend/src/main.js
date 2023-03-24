import { createApp } from "vue";
import { createPinia } from "pinia";

import BootstrapVue3 from "bootstrap-vue-3";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";

import { createAuth0 } from "@auth0/auth0-vue";

import App from "@/App.vue";
import router from "@/router";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(BootstrapVue3);
app.use(
  createAuth0({
    domain: "dev-7lc6f7vw.us.auth0.com",
    client_id: "bvznb16wbCehBiYLjXV70m90NvoMl8Gd",
    redirect_uri: window.location.origin,
    audience: "http://localhost:5000",
  })
);

library.add(fas);

app.mount("#app");
app.component("fa", FontAwesomeIcon);
