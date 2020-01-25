<template>
  <div
    id="container"
    class="row"
  >
    <div
      class="row"
      style="min-width: 45px"
    >
      <center>
        <q-icon
          color="dark"
          :name="image"
          :size="'xl'"
        />
      </center>
    </div>
    <div class="row q-pl-md q-pt-md">
      <div>{{ itemName }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeDeadlineItem',
  props: {
    itemName: String,
    image: String
  }
}
</script>

<style scoped lang="scss">
h6 {
  margin: 10px;
}
#container {
  width: 15%;
  margin-top: 10px;
  margin-bottom: 10px;
}
</style>