<!-- Vue component for displaying individual comments with upvotes and collapsible replies. -->

<template>
  <b-row v-show="active">
    <b-col sm="1" style="margin-top: -30px">
      <!-- Calling Upvote component. -->
      <Upvote
        v-bind="{
          vote_count: vote_count,
          comment_id: comment_id,
        }"
      />
    </b-col>

    <b-col sm="10">
      <!-- Calling CommentReply component for reply submission. -->
      <span class="author"
        ><b>{{ creator_username }}</b></span
      >
      <br />
      <span class="comment" style="font-size: 20px">{{ body }}</span>
      <CommentReply style="margin: 10px -8px 0px" v-bind="{
        id: comment_id,
        isArchived: archived,
      }" />
      <!-- Toggleable button to extend comment replies from parent comment, YouTube-style. -->
      <b-button
        variant="outline-dark"
        style="color: CornflowerBlue; width: 90px; border: 0px"
        v-b-toggle="'extend-' + comment_id"
        class="m-1"
        v-if="replies.length > 0"
      >
        More
        <fa icon="circle-down" />
      </b-button>
      <!-- Toggleable button to extend comment replies from parent comment, YouTube-style. -->
      <b-collapse v-bind:id="'extend-' + comment_id">
        <ul class="replies" v-if="replies.length">
          <div v-for="(item, index) in replies" :key="index">
            <!-- Calling SolutionReply component to display replies. -->
            <SolutionReply v-bind="{
              comment_id: item.comment_id,
              author_id: item.author_id,
              body: item.body,
              creator_username: item.creator_username,
            }" />
          </div>
        </ul>
      </b-collapse>
    </b-col>

    <b-col sm="1" v-if="uid == author_id">
      <!-- Dropdown for delete feature -->
      <b-dropdown no-caret variant="no-outline">
        <template #button-content>
          <fa icon="ellipsis-vertical" color="#083269" size="xl" />
        </template>
        <b-dropdown-item-button @click="del">Delete</b-dropdown-item-button>
      </b-dropdown>
    </b-col>
  </b-row>
</template>

<script>
import CommentReply from "@/components/CommentReply.vue";
import Upvote from "./Upvote.vue";
import SolutionReply from "./SolutionReply.vue";
import { useFetch } from "@/components/useFetch.vue";
import { login_state } from "@/login_state.js";

// Initially defining props, methods, and variables to be updated with information from backend.
export default {
  data() {
    return {
      uid: login_state.user_id,
      active: true,
    };
  },
  components: {
    CommentReply,
    Upvote,
    SolutionReply,
  },
  props: {
    comment_id: {
      type: Number,
      required: true,
    },
    author_id: {
      required: true,
    },
    body: {
      type: String,
      required: true,
    },
    replies: {
      type: Array,
      default: () => [],
    },
    creator_username: {
      type: String,
      required: true,
    },
    vote_count: {
      type: Number,
      required: true,
    },
    archived: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    del() {
      const config = {
        method: "PUT",
      };
      this.active = false;
      useFetch("/api/comments/user/delete/" + this.comment_id, config, true);
    },
  },
};
</script>
