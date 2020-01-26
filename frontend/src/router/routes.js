const routes = [
  { path: "", redirect: "home" },
  {
    path: "/login",
    component: () => import("pages/LoginPage.vue"),
    children: []
  },
  {
    path: "/home",
    component: () => import("layouts/MyLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Dashboard.vue") }]
  },
  {
    path: "/calendar",
    component: () => import("layouts/MyLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Calendar.vue") }]
  },
  {
    path: "/dining",
    component: () => import("layouts/MyLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Dining.vue") }]
  },
  {
    path: "/coffee",
    component: () => import("layouts/MyLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Coffee.vue") }]
  },
  {
    path: "/activities",
    component: () => import("layouts/MyLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Activities.vue") }]
  },
  {
    path: "/learning",
    component: () => import("layouts/MyLayout.vue"),
    meta: { requiresAuth: true },
    children: [{ path: "", component: () => import("pages/Learning.vue") }]
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
