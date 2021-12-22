from collections import defaultdict


MIN_BEACONS = 12
MIN_EDGES = ((MIN_BEACONS - 1) * MIN_BEACONS) / 2


def matrix_mul(m1, m2):
    product = lambda row, col: m1[3 * row] * m2[col] + m1[3 * row + 1] * m2[3 + col] + m1[3 * row + 2] * m2[6 + col]
    return tuple(product(row, col) for row in range(3) for col in range(3))


def vector_matrix_mul(point, m):
    x, y, z = point
    xr = x * m[0] + y * m[3] + z * m[6]
    yr = x * m[1] + y * m[4] + z * m[7]
    zr = x * m[2] + y * m[5] + z * m[8]
    return (xr, yr, zr)


def vector_diff(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])


def manhattan(p1, p2):
    return sum(abs(v) for v in vector_diff(p1, p2))


class Rotations:
    def __init__(self):
        Iden = (1, 0, 0, 0, 1, 0, 0, 0, 1)
        rotX = (1, 0, 0, 0, 0, -1, 0, 1, 0)
        rotY = (0, 0, -1, 0, 1, 0, 1, 0, 0)
        rotZ = (0, 1, 0, -1, 0, 0, 0, 0, 1)

        rotYY = matrix_mul(rotY, rotY)
        rotYYY = matrix_mul(rotYY, rotY)
        rotXX = matrix_mul(rotX, rotX)
        rotXXX = matrix_mul(rotXX, rotX)
        rotZZZ = matrix_mul(matrix_mul(rotZ, rotZ), rotZ)

        yRot = (Iden, rotY, rotYY, rotYYY)
        ortoRot = (Iden, rotX, rotXX, rotXXX, rotZ, rotZZZ)

        self.rotations = [matrix_mul(o, y) for o in ortoRot for y in yRot]


    def detect_orientation(self, pairs):
        ref, other = pairs[0]
        ref_points = [vector_diff(ref_next, ref) for ref_next, _ in pairs[1:]]
        other_points = [vector_diff(other_next, other) for _, other_next in pairs[1:]]

        for idx in range(len(self.rotations)):
            rotated = self.rotate_to(idx, other_points)
            if ref_points == rotated:
                return idx

        assert False


    def rotate_to(self, rotation, points):
        return [self.rotate_point(rotation, point) for point in points]


    def rotate_point(self, rotation, point):
        return vector_matrix_mul(point, self.rotations[rotation])


class Matcher:
    def __init__(self, edges_other):
        self.by_distance = defaultdict(list)
        self.mapping = []

        for point1, dist, point2 in edges_other:
            self.by_distance[dist].append((point1, point2))


    def match(self, edges):
        assert self.match_exactly(edges)
        return set(self.mapping)


    def match_exactly(self, edges, pos = 0):
        if pos == len(edges):
            return True

        point1, dist, point2 = edges[pos]
        for other_point1, other_point2 in self.by_distance[dist]:
            if self.push_mapping(point1, point2, other_point1, other_point2):
                if self.match_exactly(edges, pos + 1):
                    return True

                self.pop_mapping()

            if self.push_mapping(point1, point2, other_point2, other_point1):
                if self.match_exactly(edges, pos + 1):
                    return True

                self.pop_mapping()

        return False


    def push_mapping(self, p1, p2, o1, o2):
        for frm, to in self.mapping:
            if (frm == p1 and to != o1) or (frm == p2 and to != o2):
                return False

        self.mapping.append((p1, o1))
        self.mapping.append((p2, o2))
        return True


    def pop_mapping(self):
        self.mapping.pop()
        self.mapping.pop()


class Scanner:
    rotations = Rotations()

    def __init__(self, beacons):
        self.distances = defaultdict(list)
        self.beacons = beacons
        self.merged = []

        for idx1, p1 in enumerate(beacons):
            for idx2, p2 in enumerate(beacons[idx1 + 1:]):
                self.distances[self.distance(p1, p2)].append((idx1, idx1 + 1 + idx2))


    def merge(self, scanner):
        matching_dist = self.distances.viewkeys() & scanner.distances.viewkeys()
        if len(matching_dist) < MIN_EDGES:
            return False


        edges_ref = self.connected_edges(matching_dist)
        edges_other = scanner.connected_edges(matching_dist)
        if edges_ref is None or edges_other is None:
            return False

        matcher = Matcher(edges_other)
        mapping = matcher.match(edges_ref)
        matching_beacons = [(self.beacons[frm], scanner.beacons[to]) for frm, to in mapping]
        rotation = self.rotations.detect_orientation(matching_beacons)

        ref, other = matching_beacons[0]
        xs, ys, zs = vector_diff(self.rotations.rotate_point(rotation, other), ref)

        check = set(self.beacons)
        for x, y, z in self.rotations.rotate_to(rotation, scanner.beacons):
            point = (x + xs, y + ys, z + zs)
            if point not in check:
                self.add_beacon(point)

        self.merged.append((xs, ys, zs))
        return True


    def connected_edges(self, matching_dist):
        seen = defaultdict(list)
        for dist in matching_dist:
            for point1, point2 in self.distances[dist]:
                seen[point1].append(point2)
                seen[point2].append(point1)

        candidate_sets = [(point, set(points + [point])) for point, points in seen.items() if len(points) >= MIN_BEACONS - 1]
        candidate_sets.sort(key=lambda candidate: len(candidate[1]), reverse=True)

        for idx, (_, joint_set) in enumerate(candidate_sets):
            joint_set = self.try_point_set(joint_set, candidate_sets[idx + 1:])
            if joint_set is not None:
                edges = []
                for dist in matching_dist:
                    edges.extend((point1, dist, point2) for point1, point2 in self.distances[dist] if point1 in joint_set and point2 in joint_set)

                if len(edges) >= MIN_EDGES:
                    return edges

        return None


    def try_point_set(self, joint_set, candidate_sets):
        for point, candidate_set in candidate_sets:
            candidate = joint_set & candidate_set
            if len(candidate) >= MIN_BEACONS:
                joint_set = candidate
            else:
                joint_set.remove(point)
                if len(joint_set) < MIN_BEACONS:
                    return None

        return joint_set


    def add_beacon(self, beacon):
        nx, ny, nz = beacon
        for idx, point in enumerate(self.beacons):
            self.distances[self.distance(beacon, point)].append((idx, len(self.beacons)))

        self.beacons.append(beacon)


    def distance(self, p1, p2):
        dx, dy, dz = vector_diff(p1, p2)
        return dx * dx + dy * dy + dz * dz


with open("day19.txt") as file:
    scanners = [Scanner([(int(x), int(y), int(z)) for x, y, z in (beacon.split(',') for beacon in part.split("\n")[1:])]) for part in file.read().strip().split("\n\n")]

    root = scanners[0]
    merged = set()
    while len(merged) != len(scanners) - 1:
        for idx, scanner in enumerate(scanners[1:]):
            if idx not in merged:
                if root.merge(scanner):
                    merged.add(idx)

    print "Part 1: {}".format(len(root.beacons))

    scn = root.merged + [(0, 0, 0)]
    print "Part 2: {}".format(max(manhattan(pos1, pos2) for idx, pos1 in enumerate(scn) for pos2 in scn[idx + 1:]))
