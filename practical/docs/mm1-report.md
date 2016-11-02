<div align="center">
    <img src="university-of-edinburgh-logo.png" width="30%">

    <h5>Robotics: Science and Systems</h5>

    Major Milestone 1 - Report
    <sup><h6>October 19th, 2016</h6></sup>

    <sup>Group 9 - Henrique Ferrolho and Jacob Longval</sup>
</div>


##### Design

- Two front wheels - using 5:3 gearing ratio
- Small pivot wheel at the front, connected to Hall input
- Steel ball caster at the back
- Two IR sensors at the front, slightly angled outwards
- Two whiskers at the front, covering the IR sensors blind angle


##### Control

- Reactive behavior:
    - Go forward
    - Use IR sensors to change direction
    - Listen to whiskers for imminent frontal collisions
- Detects and resolves when stuck in corner


##### Vision

- Constantly queries camera for frames at *medium* resolution
- Crops region of interest from frame
- Uses *SIFT* for *Feature Matching + Homography* to scan for **nearby** resources and identify them
- Filters frame based on HSV range, and calculates *centroids* of the *mask contours* to identify **distant** objects of interest
