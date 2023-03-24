import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import DiscussionBoard from "@/views/DiscussionBoard.vue";
import ViewPost from "@/views/ViewPost.vue";
import Admin from "@/views/AdminView.vue";
import LoginView from "@/views/LoginView.vue";
import ProfilePage from "@/views/ProfilePage.vue";
import SubmitPost from "@/views/SubmitPost.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/discussion-board",
    name: "Discussion Board",
    component: DiscussionBoard,
  },
  {
    path: "/admin",
    name: "Admin",
    component: Admin,
  },
  {
    path: "/view-post/:id",
    name: "View Post :id",
    component: ViewPost,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
  {
    path: "/profile-page",
    name: "Profile",
    component: ProfilePage,
  },
  {
    path: "/submit-post",
    name: "Submit Post",
    component: SubmitPost,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

//This was for the tests
export { routes };

export default router;
