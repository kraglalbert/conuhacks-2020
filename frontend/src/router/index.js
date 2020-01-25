import Vue from "vue";
import VueRouter from "vue-router";

import axios from "axios";
import routes from "./routes";
import Store from "../store";

Vue.use(VueRouter);

var config = require("../config");

// Axios config
const frontendUrl = config.build.host + ":" + config.build.port;
const backendUrl = config.build.backendHost + ":" + config.build.backendPort;

var AXIOS = axios.create({
  baseURL: backendUrl,
  headers: {
    "Access-Control-Allow-Origin": frontendUrl,
    "Content-Type": "application/json"
  }
});

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation
 */

export default function(/* { store, ssrContext } */) {
  const Router = new VueRouter({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes,

    // Leave these as is and change from quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    mode: process.env.VUE_ROUTER_MODE,
    base: process.env.VUE_ROUTER_BASE
  });

  Router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      // this route requires auth, check if logged in
      // if not, redirect to login page.
      if (!Store.getters.isLoggedIn) {
        next({
          path: "/login",
          query: { redirect: to.fullPath }
        });
      } else if (Store.getters.isLoggedIn && !Store.state.userExists) {
        // get user with stored token
        const token = Store.state.token;
        AXIOS.post("/account/token", { token: token })
          .then(resp => {
            Store.commit("set_user", resp.data);
            next();
          })
          .catch(() => {
            // token is invalid
            Store.dispatch("logout").then(
              next({
                path: "/login",
                query: { redirect: to.fullPath }
              })
            );
            next();
          });
      } else {
        next();
      }
    } else {
      next(); // always call next()
    }
  });

  return Router;
}
