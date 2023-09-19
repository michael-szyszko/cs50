#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

void swap (pair* p1, pair* p2);
bool cycle (int winner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{

    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // preferences[i][j] is number of voters who prefer i over j
    //int preferences[MAX][MAX];
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]] += 1;
            printf("%i\n", preferences[ranks[i]][ranks[j]]);
        }
        // ranks[i] contains indices of candidates in order of preference, e.g., ranks[0] will contain the voters first choice while rank[candidate_count] contains the index of the last choice
        // Alice Bob Charlie, ranks {1, 0, 2} (2+1 =3)
        // preferences[0][0] = 0, preferences [0][1] = 0, preferences[0][2] = +=1
        // preferences[1][0] = +=1, preferences [1][1] = 0, preferences[1][2] = +1
        // preferences[2][0] = 0, preferences [2][1] = 0, preferences[2][2] = 0

        // Alice Bob Charlie, Daniel ranks {1, 0, 3, 2} (3+2+1=6)
        // preferences[0][0] = 0, preferences [0][1] = 0, preferences[0][2] = +=1, preferences[0][3] = +=1
        // preferences[1][0] = +1, preferences [1][1] = 0, preferences[1][2] = +=1, preferences[1][3] = +=1
        // preferences[2][0] = 0, preferences [2][1] = 0, preferences[2][2] = 0, preferences[2][3] = 0
        // preferences[3][0] = 0, preferences [3][1] = 0, preferences[3][2] = +=1, preferences[3][3] = 0

        // Alice Bob Charlie, Daniel, Evan ranks {1, 0, 3, 2, 4} (4+3+2+1=10)
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            //some candidates will be tied between eachother, and when i == j, the value is always 0
            if (preferences[i][j] != preferences[j][i])
            {
                //printf("preferences[%i][%i]:%i preferences[%i][%i]: %i\n", i,j,preferences[i][j],j,i,preferences[j][i]);
                // copy and pasted assignment, opportunity to refactor here
                if (preferences[i][j] > preferences[j][i])
                {
                    pairs[pair_count].winner = i;
                    pairs[pair_count].loser = j;
                }
                else
                {
                    pairs[pair_count].winner = j;
                    pairs[pair_count].loser = i;
                }
                pair_count += 1;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - i - 1; j++)
        {
            //swap if the current pair has greater strength of victory
            if (preferences[pairs[j].winner][pairs[j].loser] < preferences[pairs[j+1].winner][pairs[j+1].loser])
            {
                swap(&pairs[j], &pairs[j+1]);
            }
        }
    }
    return;
}

void swap (pair* p1, pair* p2)
{
    pair temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // locked[i][j] means i is locked in over j
    for (int i = 0; i < pair_count; i++)
    {
        if (!cycle(pairs[i].winner, pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// move up the graph by closest connections recursively. If the loser is a winner in the graph already connectet then this would create a cycle.
bool cycle (int winner, int loser)
{
    if (locked[winner][loser])
    {
        return true;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[i][winner])
        {
            if (cycle(i, winner))
            {
                return true;
            }
        }
    }
    return false;
}

// Print the winner of the election
void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool edges = false;
        for (int j = 0; j < candidate_count; j++)
        {
            //if there are any edges on the candidate, they are not the winner
            if(locked[j][i] == true)
            {
                edges = true;
            }
        }
        //the candidate has no edges meaning they are the winner
        if (edges == false)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
    return;
}