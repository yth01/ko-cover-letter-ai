<template>
    <div id="input-field">
        <div id="input-field-header">input-header</div>
        <input type="text" v-model="input">
        <div id="input-field-footer">input-footer</div>
    </div>
</template>

<script>
export default {
    data: function () {
        return {
            input: ''
        }
    },
}
</script>

<style scoped>
#input-field {
    /* Auto layout */
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>