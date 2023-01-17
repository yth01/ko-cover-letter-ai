<template>
    <footer>
        <font-awesome-icon icon="fa-brands fa-github" v-on:click="MoveGithubProfile" v-on:mouseover="HighlightingIcon"
            v-on:mouseout="RevertingIcon" v-bind:style="{ opacity: computedOpacity }" />
        <p>Copyright 2022. yth01 | All Rights Reserved</p>
    </footer>
</template>

<script>
export default {
    data: function () {
        return {
            opacity: 0.7
        }
    },
    computed: {
        computedOpacity: function () {
            return this.opacity
        }
    },
    methods: {
        MoveGithubProfile: function () {
            window.open("https://www.github.com/yth01")
        },
        HighlightingIcon: function () {
            this.opacity = 1
        },
        RevertingIcon: function () {
            this.opacity = 0.7
        }
    }
}
</script>

<style scoped>
footer {
    /* Auto layout */
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;

    height: 55px;
    position: fixed;
    bottom: 0;
    width: 100%;
}

p {
    margin-left: 10px;
    font-family: NanumSquareNeo-cBd;
    font-size: x-small;
    opacity: 0.3;
}
</style>