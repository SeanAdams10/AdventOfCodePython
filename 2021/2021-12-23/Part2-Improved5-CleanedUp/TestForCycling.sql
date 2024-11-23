select fingerprint 
from dbo.IterationOutput
where Explore=1
order by 

select 
	Fingerprint, count(distinct(IterNo))
from
	IterationOutput with (nolock)
where Explore =1
Group by Fingerprint





select 
	* 
from
	IterationOutput with (nolock)
where IterNo = 0



select iterno, count(fingerprint) as fingerprintCount
from IterationOutput with (nolock)
Group by iterno
order by fingerprintCount asc


Truncate table IterationOutput
truncate table dbo.ExploreIteration
truncate table dbo.ExplorePostIteration



select count(*) 
from IterationOutput




with ranker as(
select fingerprint, iterno, etc, mincost, rank()
	over(partition by iterno
		order by explore desc, etc asc, mincost asc, fingerprint asc) as RowRank
from 
	dbo.IterationOutput
) 
select ranker.Fingerprint, ranker.IterNo, ranker.MinCost, ranker.ETC, io.iterno, io.MinCost, io.ETC 
from 
	ranker
	inner join 	dbo.IterationOutput IO
		on IO.fingerprint = ranker.fingerprint
		and IO.IterNo > ranker.iterNo
		and IO.explore = 1
order by ranker.fingerprint, ranker.IterNo, io.IterNo



-- Look for things that went into the path finder, but didn't get marked as explored
select 
	EI.fingerprint, 
	count(EI.Fingerprint) over (partition by EI.fingerprint) as instanceCount,
	EI.iterno, 
	EI.mincost, EI.DistanceToGoal, io.iterno, io.MinCost, io.ETC, IO.DistanceToGoal
from 
	dbo.exploreIteration EI with (nolock)
	inner join 	dbo.IterationOutput IO with (nolock)
		on IO.fingerprint = EI.fingerprint
		and IO.IterNo > EI.iterNo
		and IO.explore = 1
order by InstanceCount desc, EI.fingerprint, eI.IterNo, io.IterNo


-- Look at where something went from Non-explore state to Explore state
Select 
	E1.fingerprint, E1.MinCost, e1.DistanceToGoal, E2.MinCost, e2.DistanceToGoal
from
	dbo.IterationOutput E1 with(nolock)
	Inner join dbo.IterationOutput E2 with (nolock)
		on E1.Fingerprint = E2.Fingerprint
		and E1.iterno+1 = E2.iterno
		and E1.explore = 0 
		and e2.explore = 1
		and e2.MinCost >= e1.MinCost



-- look for the Target State for part 2 test example - cost should be 44169
Select * 
from IterationOutput with (nolock)
where 
	   fingerprint = 3826169111163756 --step 5

	or fingerprint = 11916152941875000 --endstate
order by iterno, mincost





-- look for duplicate fingerprints in the same iteration
select fingerprint, iterNo, count(*)
from 
	dbo.IterationOutput with (nolock)
group by fingerprint, iterNo
having count(*) > 1



select top(3) *
from IterationOutput
order by DistanceToGoal asc


-- are the distances getting better?
select 
	iterno, 
	min(distanceToGoal) as DistanceToGoal, 
	min(ETC) as minETC, 
	count(*) as recordCount, 
	sum(explore) as exploreCount, 
	(sum(explore)*100)/count(*) as PercToExplore
from IterationOutput with (nolock)
group by iterno
order by iterno desc


Select mincost, count(*) as exploreCount
from IterationOutput with (nolock)
where IterNo = 
	(select max(iterno) 
	from IterationOutput with (nolock))
	and explore = 1
group by mincost
order by mincost asc

with currentIter as (
	Select DistanceToGoal, count(*) as exploreCount,max(iterno) as iterno
	from IterationOutput with (nolock)
	where IterNo = 
		(select max(iterno) 
		from IterationOutput with (nolock))
		and explore = 1
	group by DistanceToGoal
), prevIter as (
	Select DistanceToGoal, count(*) as exploreCount
	from IterationOutput with (nolock)
	where IterNo = 
		(select max(iterno) 
		from IterationOutput with (nolock))-1
		and explore = 1
	group by DistanceToGoal
), previter2 as (
	Select DistanceToGoal, count(*) as exploreCount
	from IterationOutput with (nolock)
	where IterNo = 
		(select max(iterno) 
		from IterationOutput with (nolock))-2
		and explore = 1
	group by DistanceToGoal
)
select 
	currentIter.DistanceToGoal,
	currentiter.iterno,
	currentiter.exploreCount as currentCount,
	previter.exploreCount as "Current-1",
	previter2.exploreCount as "Current-2"
from
	currentIter full outer join prevIter
		on currentIter.DistanceToGoal = prevIter.DistanceToGoal
	full outer join previter2
			on prevIter.DistanceToGoal = prevIter2.DistanceToGoal
Order by DistanceToGoal asc