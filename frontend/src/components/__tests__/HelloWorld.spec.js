import { describe, it, test, expect } from "vitest";
import { mount, flushPromises } from "@vue/test-utils";

import { createRouter, createWebHistory } from "vue-router";
import { routes } from "@/router/index.js";

import App from "@/App.vue";
import HomeView from "@/views/HomeView.vue";
import DiscussionBoard from "@/views/DiscussionBoard.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

//Page when website is open
it("routing", () => {
  const wrapper = mount(HomeView);
  expect(wrapper.html()).toContain("Welcome to TAWC Power Room");
});

//Testing the connection between routes - attempt 1
//failed as cannot find Dolphin in the html div.
it("go to discussion board", async () => {
  router.push("/");

  // After this line, router is ready
  await router.isReady();

  const wrapper = mount(HomeView, {
    global: {
      plugins: [router],
    },
  });
  expect(wrapper.html()).toContain("Welcome to TAWC Power Room");
  const discussionboard_link = wrapper.find("#discussionboard_link");
  expect(discussionboard_link.element.id).toBe("discussionboard_link");

  await wrapper.find("#discussionboard_link").trigger("click");
  await flushPromises();

  console.log(wrapper.html());
  expect(wrapper.html()).toContain("dolphin");
});

//Testing the connection between routes - attempt 2
//Works better but for some reason its getting false.
/*
describe("App", () => {
  it("renders a component via routing", async () => {
    // create local router
    const router = createRouter({
      history: createWebHistory(),
      routes: routes,
    });

    // navigate to route
    router.push("/discussion-board");

    // await navigation from push()
    await router.isReady();

    // install the local router
    const wrapper = mount(HomeView, {
      global: {
        plugins: [router],
      },
    });

    expect(wrapper.findComponent(DiscussionBoard).exists()).toBe(true);
  });
});
*/
