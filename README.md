# Simulation of a simple state saving mechanism

Simulation of saving state from data processing task when: given interrupt signal `ctrl + c`, have processed certain number of instances, or certain number of time has elapsed.

**THE CODE IS STILL MESSY**

## Motivation

I did several web scraping/data fetching tasks these past few months. I ran the tasks on my laptop, and some tasks took too long and I have to wait for it to finish before I could shut down, just because it won't continue from the last time it processed things. That was when I thought a **continue from this previous state/line** mechanism would be useful, and I started to implement it in my last program. The implementation was kinda sloppy and I wonder whether there's a better way of doing it, maybe creating a utility class that can easily be imported or extended in some way that can provide that kind of mechanism.

That's why I started this simulation as a means for exploration of what could be done (and a means of learning).

## **TODO**

- [x] Simulate state saving on interrupt signal (`ctrl +c`)
- [x] Simulate state saving on number of instance processed
- [x] Simulate state saving on time elapsed
- [ ] Create a utility state saving class based on interrupt, instance processed, and time elapsed

## How It's Going

The code is still messy and I'm still trying to figure out what's the best way to implement the utility class. It's at least these things:

- A loop of `process_state` procedure that do some work (I imagine requesting page from the web) that took some time (simulated by `sleep`)
- A `dump` procedure that save the state onto a file
- An `interrupt_handler`, `save_by_n_processed`, and `save_by_t_elapsed` decorators that is used on the `process_state` to keep track of calls and state update
- A `handler` (register?) that knit the decorators, `process_state`, and state together

For now, there's three things I want to keep here as reminder:

1. There's three way of saving state, two which doesn't depend on the user: instances processed (`n`) and time elapsed (`t`). These two might "crash" when used together. For an example, try to simulate process that run for 1 second, save state after processing 10 instances and also every 1 minutes. This scenario would "crash" when after processing 60 instances (1s each) the state is saved by `n` AND is saved AGAIN by `t`. This scenario is still sequential in nature, but there's some sort of logical unease here that should be pointed out.
2. The assumption above is true when `n` and `t` are both set, still it's only an asummption. As, the user may prefer not to use both of them at the same time in the first place (and the choice could be given to them) because both `n` and `t` achieve the same result only through different means: do you care about the instances already processed or the time that had elapsed? The task then, is to make the transition from `n` to `t` as seamless as possible.
3. (though the second assumption is stronger, I want to state here). To prevent the error of `n` and `t` "crashing" at the same time, a `CalledTooOftenError` exception can be implemented (example from Reuven). In the current implementation, both `n` and `t` uses `dumps` procedure to save state, so `CalledTooOftenError` might be set on `dumps` when the program tries to save state too often in short period of time

## Useful Links

- [Practical Decorators by Reuven M. Lerner on PyCon2019](https://youtu.be/MjHpMCIvwsY)
