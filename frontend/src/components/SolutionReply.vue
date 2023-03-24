<!-- Vue component for displaying individual replies to parent comments. -->

<template>
  <!-- Displays reply author and content. -->
  <p v-show="active">
    <span class="author"
      ><b>{{ creator_username }}</b></span
    >
    <!-- Dropdown for delete feature -->
    <b-dropdown
      v-if="uid == author_id"
      no-caret
      variant="no-outline"
      style="border: 0px solid white"
    >
      <template #button-content>
        <fa icon="ellipsis-vertical" color="#083269" />
      </template>
      <b-dropdown-item-button @click="del" style="border: 0 sold grey"
        >Delete</b-dropdown-item-button
      >
    </b-dropdown>
    <br />
    <span class="comment">{{ body }}</span>
  </p>
</template>

<script>
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
    creator_username: {
      type: String,
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
