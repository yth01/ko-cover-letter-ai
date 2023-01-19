<template>
    <footer>
        <v-btn id="footer-icon" icon color="black" v-on:click="moveGithubProfile" v-on:mouseover="highlightingIcon"
            v-on:mouseout="revertingIcon" v-bind:style="{ opacity: iconOpacity }">
            <v-icon>mdi-github</v-icon>
        </v-btn>
        <div id="footer-text">Copyright 2022. yth01 | All Rights Reserved</div>
    </footer>
</template>

<script>
export default {
    data: function () {
        return {
            iconOpacity: 0.7
        }
    },
    methods: {
        moveGithubProfile: function () {
            window.open("https://www.github.com/yth01")
        },
        highlightingIcon: function () {
            this.iconOpacity = 1
        },
        revertingIcon: function () {
            this.iconOpacity = 0.7
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

#footer-text {
    font-family: NanumSquareNeo-cBd;
    font-size: x-small;
    opacity: 0.3;
}
</style>