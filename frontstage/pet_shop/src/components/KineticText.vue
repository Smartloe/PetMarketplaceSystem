<template>
  <span class="kinetic">
    <!-- aria-label on a role-less span is not reliably exposed, so the readable
         copy is a real text node kept off-screen instead. -->
    <span class="kinetic-sr">{{ readableText }}</span>

    <span
      v-for="(line, lineIndex) in lines"
      :key="`line-${lineIndex}`"
      class="kinetic-line"
      :style="{ '--line-delay': `${lineIndex * lineStagger}ms` }"
      aria-hidden="true"
    >
      <span
        v-for="segment in line.segments"
        :key="`seg-${lineIndex}-${segment.start}`"
        class="kinetic-segment"
        :class="{ 'kinetic-accent': segment.accent }"
      >
        <span
          v-for="(char, charIndex) in segment.chars"
          :key="`char-${lineIndex}-${segment.start}-${charIndex}`"
          class="kinetic-char"
          :style="{ '--char-index': segment.start + charIndex }"
        >{{ char }}</span>
      </span>
    </span>
  </span>
</template>

<script>
import { computed } from 'vue';

/*
 * Splits a headline into per-character spans so CSS can choreograph it.
 *
 * Authoring syntax:
 *   `|`      an explicit line break
 *   `*...*`  an accented run, anywhere within a line
 *
 * The plain sentence is rendered once as off-screen text and the animated
 * spans are aria-hidden, so assistive tech reads the headline exactly once.
 */
export default {
  name: 'KineticText',
  props: {
    text: {
      type: String,
      required: true,
    },
    lineStagger: {
      type: Number,
      default: 90,
    },
  },
  setup(props) {
    const lines = computed(() =>
      props.text.split('|').map((rawLine) => {
        // Odd indices are the runs that sat between a pair of asterisks.
        const parts = rawLine.split('*');
        let cursor = 0;
        const segments = [];

        parts.forEach((part, partIndex) => {
          if (!part) {
            return;
          }
          const chars = Array.from(part);
          segments.push({
            accent: partIndex % 2 === 1,
            chars,
            // Character offset within the line, so the stagger stays continuous
            // across segment boundaries.
            start: cursor,
          });
          cursor += chars.length;
        });

        return { segments };
      })
    );

    // Markers are authoring syntax, never spoken content.
    const readableText = computed(() => props.text.replace(/[|*]/g, ''));

    return { lines, readableText };
  },
};
</script>

<style scoped>
.kinetic-segment {
  display: inline;
}

.kinetic-accent {
  color: var(--vermilion-deep);
}

/* Visually hidden, still read aloud and still found by in-page search. */
.kinetic-sr {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
  border: 0;
}
</style>
