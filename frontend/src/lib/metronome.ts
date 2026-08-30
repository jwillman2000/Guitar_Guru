// Web Audio look-ahead scheduler (the standard "two clocks" pattern) — per
// CONSTITUTION.md Article V, metronome timing must come from the audio
// clock, never setInterval/setTimeout directly triggering sound.
//
// setInterval below is only a low-frequency *re-check* loop: on each tick it
// looks ahead a short window and schedules any beats due in that window via
// AudioContext.currentTime-based times (oscillator.start(preciseTime)).
// Actual audio timing is sample-accurate because it comes from the audio
// clock, not from when the JS timer happens to fire.

const LOOKAHEAD_MS = 25 // how often the scheduler re-checks
const SCHEDULE_AHEAD_SECONDS = 0.1 // how far into the future to schedule beats
const CLICK_DURATION_SECONDS = 0.05

export interface Metronome {
  start(): void
  stop(): void
  setBpm(bpm: number): void
  isPlaying(): boolean
}

export function createMetronome(initialBpm: number, onBeat?: (time: number) => void): Metronome {
  let bpm = initialBpm
  let audioContext: AudioContext | null = null
  let nextBeatTime = 0
  let timerId: ReturnType<typeof setInterval> | null = null

  function scheduleClick(time: number) {
    if (!audioContext) return
    const osc = audioContext.createOscillator()
    const gain = audioContext.createGain()
    osc.frequency.value = 1000
    gain.gain.setValueAtTime(1, time)
    gain.gain.exponentialRampToValueAtTime(0.001, time + CLICK_DURATION_SECONDS)
    osc.connect(gain)
    gain.connect(audioContext.destination)
    osc.start(time)
    osc.stop(time + CLICK_DURATION_SECONDS)
    onBeat?.(time)
  }

  function tick() {
    if (!audioContext) return
    while (nextBeatTime < audioContext.currentTime + SCHEDULE_AHEAD_SECONDS) {
      scheduleClick(nextBeatTime)
      nextBeatTime += 60 / bpm
    }
  }

  return {
    start() {
      if (timerId !== null) return
      audioContext = new AudioContext()
      nextBeatTime = audioContext.currentTime
      tick()
      timerId = setInterval(tick, LOOKAHEAD_MS)
    },
    stop() {
      if (timerId !== null) {
        clearInterval(timerId)
        timerId = null
      }
      void audioContext?.close()
      audioContext = null
    },
    setBpm(newBpm: number) {
      bpm = newBpm
    },
    isPlaying() {
      return timerId !== null
    },
  }
}
