<template>
    <div>
        <div class="text-h4 q-mb">{{event.name}}</div>
        <p>{{event.description}}</p>
    </div>
</template>

<script>
import moment from "moment";

export default {
  name: 'CalendarItemList',
  props: {
    event: Object
  }
}
</script>