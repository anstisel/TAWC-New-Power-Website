<template>
  <div>
    <!-- Questions Tab -->
    <b-tabs lazy active-nav-item-class="text-warning">
      <!-- Questions tab -->
      <b-tab title="Questions">
        <b-card v-if="posts.length === 0">There is nothing yet! :]</b-card>
        <div v-for="i in posts" :key="i.post_id">
          <AdminPost
            v-bind="{
              id: i.post_id,
              pid: i.post_id,
              title: i.title,
              username: i.creator_username,
              date: i.create_time,
              details: i.body,
              avatar: i.creator_avatar,
              comment: false,
            }"
          />
        </div>
      </b-tab>

      <!-- Solutions Tab -->
      <b-tab title="Solutions">
        <b-card v-if="sols.length === 0">There is nothing yet! :]</b-card>
        <div v-for="i in sols" :key="i.comment_id">
          <AdminPost
            v-bind="{
              id: i.comment_id,
              pid: i.post_id,
              username: i.creator_username,
              date: i.create_time,
              avatar: i.creator_avatar,
              details: i.body,
            }"
          />
        </div>
      </b-tab>


      <!-- Comments tab with sub-tabs for Replies, Clarifications and Others -->
      <b-tab title="Comments">
        <b-tabs lazy active-nav-item-class="text-warning">
          <b-tab title="Replies" title-link-class="tab">
            <b-card v-if="replies.length === 0"
              >There is nothing yet! :]</b-card
            >
            <div v-for="i in replies" :key="i.comment_id">
              <AdminPost
                v-bind="{
                  id: i.comment_id,
                  pid: i.post_id,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  avatar: i.creator_avatar,
                }"
              />
            </div>
          </b-tab>

          <!-- Comments: Clarifications Tab -->
          <b-tab title="Clarifications" title-link-class="tab">
            <b-card v-if="clarifs.length === 0"
              >There is nothing yet! :]</b-card
            >
            <div v-for="i in clarifs" :key="i.comment_id">
              <AdminPost
                v-bind="{
                  id: i.comment_id,
                  pid: i.post_id,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  avatar: i.creator_avatar,
                }"
              />
            </div>
          </b-tab>

          <!-- Comments: Other Tab -->
          <b-tab title="Other" title-link-class="tab">
            <b-card v-if="others.length === 0">There is nothing yet! :]</b-card>
            <div v-for="i in others" :key="i.comment_id">
              <AdminPost
                v-bind="{
                  id: i.comment_id,
                  pid: i.post_id,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  avatar: i.creator_avatar,
                }"
              />
            </div>
          </b-tab>
        </b-tabs>
      </b-tab>


      <!-- History tab shows past Admin actions -->
      <b-tab title="History">
        <b-tabs lazy active-nav-item-class="text-warning">
          <!-- History: Questions Tab -->
          <b-tab title="Questions">
            <b-card v-if="mod_posts.length === 0"
              >There is nothing yet! :]</b-card
            >
            <div v-for="i in mod_posts" :key="i.post_id">
              <AdminPost
                v-bind="{
                  id: i.post_id,
                  pid: i.post_id,
                  title: i.title,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  approved: i.approved,
                  archived: i.archived,
                  comment: false,
                  history: true,
                  avatar: i.creator_avatar,
                }"
              />
            </div>
            <b-pagination
              v-model="currentPage"
              :total-rows="rows"
              :per-page="perPage"
              align="center"
              size="lg"
            ></b-pagination>
          </b-tab>

          <!-- History: Solutions Tab -->
          <b-tab title="Solutions">
            <b-card v-if="mod_sols.length === 0"
              >There is nothing yet! :]</b-card
            >
            <div v-for="i in mod_sols" :key="i.comment_id">
              <AdminPost
                v-bind="{
                  id: i.comment_id,
                  pid: i.post_id,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  approved: i.approved,
                  history: true,
                  avatar: i.creator_avatar,
                }"
              />
            </div>
            <b-pagination
              v-model="currentPagesol"
              :total-rows="rowssol"
              :per-page="perPagesol"
              align="center"
              size="lg"
            ></b-pagination>
          </b-tab>

          <!-- History: Replies Tab -->
          <b-tab title="Replies">
            <b-card v-if="mod_replies.length === 0"
              >There is nothing yet! :]</b-card
            >
            <div v-for="i in mod_replies" :key="i.comment_id">
              <AdminPost
                v-bind="{
                  id: i.comment_id,
                  pid: i.post_id,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  approved: i.approved,
                  history: true,
                  avatar: i.creator_avatar,
                }"
              />
            </div>
            <b-pagination
              v-model="currentPagerep"
              :total-rows="rowsrep"
              :per-page="perPagerep"
              align="center"
              size="lg"
            ></b-pagination>
          </b-tab>

          <!-- History: Clarifications Tab -->
          <b-tab title="Clarifications">
            <b-card v-if="mod_clarifs.length === 0"
              >There is nothing yet! :]</b-card
            >
            <div v-for="i in mod_clarifs" :key="i.comment_id">
              <AdminPost
                v-bind="{
                  id: i.comment_id,
                  pid: i.post_id,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  approved: i.approved,
                  history: true,
                }"
              />
            </div>
            <b-pagination
              v-model="currentPageclar"
              :total-rows="rowsclar"
              :per-page="perPageclar"
              align="center"
              size="lg"
            ></b-pagination>
          </b-tab>

          <!-- History: Other Tab -->
          <b-tab title="Other">
            <b-card v-if="mod_others.length === 0"
              >There is nothing yet! :]</b-card
            >
            <div v-for="i in mod_others" :key="i.comment_id">
              <AdminPost
                v-bind="{
                  id: i.comment_id,
                  pid: i.post_id,
                  username: i.creator_username,
                  date: i.create_time,
                  details: i.body,
                  approved: i.approved,
                  history: true,
                }"
              />
            </div>
            <b-pagination
              v-model="currentPageoth"
              :total-rows="rowsoth"
              :per-page="perPageoth"
              align="center"
              size="lg"
            ></b-pagination>
          </b-tab>
        </b-tabs>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import AdminPost from "../components/AdminPost.vue";
import { login_state } from "@/login_state.js";

export default {
  components: {
    AdminPost,
  },
  data() {
    return {
      posts: [],
      sols: [],
      replies: [],
      clarifs: [],
      others: [],
      mod_posts: [],
      mod_sols: [],
      mod_replies: [],
      mod_clarifs: [],
      mod_others: [],
      login_state,

      perPage: 1,
      currentPage: 1,
      total_pages: 1,

      perPagesol: 1,
      currentPagesol: 1,
      total_pagessol: 1,

      perPagerep: 1,
      currentPagerep: 1,
      total_pagesrep: 1,

      perPageclar: 1,
      currentPageclar: 1,
      total_pagesclar: 1,

      perPageoth: 1,
      currentPageoth: 1,
      total_pagesoth: 1,

    };
  },
  computed: {
    rows() {
      console.log("total pages = ", this.total_pages);
      return this.total_pages;
    },
    rowssol() {
      return this.total_pagessol;
    },
    rowsrep() {
      return this.total_pagesrep;
    },
    rowsclar() {
      return this.total_pagesclar;
    },
    rowsoth() {
      return this.total_pagesoth;
    },
  },
  watch: {
    currentPage: function () {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      fetch(
        "/api/posts/moderated?page=" + this.currentPage + "&per_page=10",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.mod_posts = data["items"];
          console.log("this.currentpage= ", this.currentPage);
        });
    },
    currentPagesol: function () {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      fetch(
        "/api/comments/moderated?page=" + this.currentPagesol + "&per_page=10",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.mod_sols = data["items"];
        });
    },
    currentPagerep: function () {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      fetch(
        "/api/comments/moderated?type=reply&page=" +
          this.currentPagerep +
          "&per_page=10",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.mod_replies = data["items"];
        });
    },
    currentPageclar: function () {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      fetch(
        "/api/comments/moderated?type=clarification&page=" +
          this.currentPageclar +
          "&per_page=10",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.mod_clarifs = data["items"];
        });
    },
    currentPageoth: function () {
      const requestOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      };
      fetch(
        "/api/comments/moderated?type=other&page=" +
          this.currentPageoth +
          "&per_page=10",
        requestOptions
      )
        .then((response) => response.json())
        .then((data) => {
          this.mod_others = data["items"];
        });
    },
  },
  mounted() {
    if (!login_state.admin) {
      this.$router.push("/");
    }

    const requestOptions = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    /* Fetches unmoderated Questions */
    fetch("/api/posts/unmoderated", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.posts = data["items"];
      });

    /* Fetches unmoderated Solutions */

    fetch("/api/comments/unmoderated", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.sols = data["items"];
      });

    /* Fetches unmoderated Comments: Replies  */
    fetch("/api/comments/unmoderated?type=reply", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.replies = data["items"];
      });
    /* Fetches unmoderated Comments: Clarifications  */
    fetch("/api/comments/unmoderated?type=clarification", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.clarifs = data["items"];
      });
    /* Fetches unmoderated Comments: Other  */
    fetch("/api/comments/unmoderated?type=other", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.others = data["items"];
      });

    /* History: Fetches moderated questions */
    fetch("/api/posts/moderated?page=1&per_page=10", requestOptions)

      .then((response) => response.json())
      .then((data) => {
        this.mod_posts = data["items"];
        this.total_pages = data._meta["total_pages"];
      });

    /* History: Fetches moderated Solutions */
    fetch("/api/comments/moderated?page=1&per_page=10", requestOptions)
      .then((response) => response.json())
      .then((data) => {
        this.mod_sols = data["items"];
        this.total_pagessol = data._meta["total_pages"];
      });

    /* History: Fetches moderated Replies */
    fetch(
      "/api/comments/moderated?type=reply&page=1&per_page=10",
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        this.mod_replies = data["items"];
        this.total_pagesrep = data._meta["total_pages"];
      });

    /* History: Fetches moderated Clarifications */
    fetch(
      "/api/comments/moderated?type=clarification&page=1&per_page=10",
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        this.mod_clarifs = data["items"];
        this.total_pagesclar = data._meta["total_pages"];
      });

    /* History: Fetches moderated Others */
    fetch(
      "/api/comments/moderated?type=other&page=1&per_page=10",
      requestOptions
    )
      .then((response) => response.json())
      .then((data) => {
        this.mod_others = data["items"];
        this.total_pagesoth = data._meta["total_pages"];
      });
  },
};
</script>

<style scoped>
.card {
  font-size: xx-large;
  color: grey;
  text-align: center;
  margin: 40px;
  padding: 50px;
  border-radius: 15px;
}
</style>
