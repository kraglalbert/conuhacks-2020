const routes = [
  {
    path: "",
    redirect: "/home"
  },
  // {
  //   path: "/home",
  //   component: () => import("layouts/MainLayout.vue"),
  //   meta: { requiresAuth: true },
  //   children: [{ path: "", component: () => import("pages/HomePage.vue") }]
  // },
  {
    path: "/login",
    component: () => import("pages/LoginPage.vue"),
    children: []
  }
];

// Always leave this as last one
if (process.env.MODE !== "ssr") {
  routes.push({
    path: "*",
    component: () => import("pages/Error404.vue")
  });
}

export default routes;
