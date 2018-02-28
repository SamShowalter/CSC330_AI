import java.util.*;

public class GameOfNIM
{
    // Private variables for the number of sticks that also
    // Keeps track of whose turn it is.
    private int numSticks;
    //Lets the computer always start first
    private boolean humanTurn = false;

    //Constructor for the game of NIM
    //Sets the number of sticks
    public GameOfNIM(int pNumSticks)
    {
        numSticks = pNumSticks;
    }

    //Static function to verify that a given input
    //by the user is valid (a non-negative integer)
    //for the number of sticks total (also not zero)
    public static boolean validInput(String s)
    {
        try
        {
            int input = Integer.parseInt(s);
            if(input < 1)
            {
                Integer.parseInt("intentional error");
            }
            return true;
        }
        catch (Exception e)
        {
            System.out.println("\nInput invalid, please enter an non-negative integer.");
            return false;
        }
    }

    //Ensures that for a given move to pick up sticks
    //That the number chosen by either the user or
    //The computer is valid.
    //-less than number of sticks left
    //In the range 1 - 4
    public boolean validRange(int pStickPickUp)
    {
        return pStickPickUp > 0 && pStickPickUp <= 4 && pStickPickUp <= numSticks;
    }

    //Checks every iteration to see if there is
    //a winner.
    public boolean checkForWinner()
    {
        if(numSticks == 0)
        {
            return true;
        }
        return false;
    }

    //If there is a winner, then the game
    //outputs a message stating who won.
    public void findWinner()
    {
        if (humanTurn)
        {
            System.out.println("\nYOU WIN!!!!\n");
        }
        else
        {
            System.out.println("\nOh no! The computer won. Better luck next time!\n");
        }
    }



    //Dictates the actions and output for a computer's move
    //Moves for computer are chosen randomly
    //and vetted for validity (see validRange
    //and validInput)
    public void computerMove()
    {
        System.out.println("It is the computers turn to move.");
        Random r = new Random();

        //loop to make sure the computer gives valid move
        while(true)
        {
            int computerStickPickUp = r.nextInt(4) + 1;
            if(validRange(computerStickPickUp))
            {
                numSticks -= computerStickPickUp;
                System.out.println("The computer picked up " + computerStickPickUp + " stick(s). " +
                        "There are " + numSticks +  " sticks left.\n");
                return;
            }
        }

    }

    //Dictates the actions and output for a humans's move.
    //Moves for humans are
    //and vetted for validity (see validRange
    //and validInput)
    public void humanMove(int pHumanSticks)
    {
        if(humanTurn)
        {
            numSticks -= pHumanSticks;
            System.out.println("You picked up " + pHumanSticks + " stick(s). There are " + numSticks + " sticks left.\n");
        }
        else
        {
            System.out.println("ERROR! human turn called out of cycle.");
        }
    }

    //Initiates the game.
    //Gives user information about the game of NIM
    //and also prompts the user to give a number of sticks
    //Generates game object
    public static GameOfNIM initiateGame()
    {
        Scanner sc = new Scanner(System.in);
        System.out.println("Welcome to the Game of NIM!\n\n" +
                "In the game of NIM, a number of sticks is specified, and each\n" +
                "player takes a turn taking a specified number of sticks. You must\n" +
                "take at least one stick, and no more that the maximum of four.\n\n" +
                "The person (or computer) who picks up the last stick wins!\n\n" +
                "How many sticks do you want to start with?");

        while(true)
        {
            String input = sc.nextLine();
            if (validInput(input))
            {
                //sc.close();
                int sticks = Integer.parseInt(input);
                GameOfNIM game = new GameOfNIM(sticks);
                System.out.println("\nYou decided to play NIM with " + sticks +" sticks. Have fun!\n");
                return game;
            }
        }

    }

    //Main execution loop that plays the game.
    //Checking for valid input, this game loops
    //continuously until a player wins.
    public void playGame()
    {
        Scanner sc = new Scanner(System.in);

        //Loop to keep the game going
        while(true)
        {
            if (humanTurn)
            {
                System.out.println("It is your turn, how many sticks would you like to pick up?");

                //Loop to iterate and find a suitable input from user.
                while(true)
                {
                    if (sc.hasNext())
                    {
                        String humanStickPickUp = sc.nextLine();
                        if(validInput(humanStickPickUp))
                        {
                            int humanSticks = Integer.parseInt(humanStickPickUp);
                            if (validRange(humanSticks))
                            {
                                humanMove(humanSticks);
                                if (checkForWinner()) {
                                    findWinner();
                                    sc.close();
                                    return;
                                }
                                humanTurn = false;
                                break;
                            }
                            else
                            {
                                System.out.println("\nINVALID INPUT: Please enter an integer between 1 and 4\n" +
                                        "That is also less than the remaining number of sticks.\n" +
                                        "Currently there are only " + numSticks + " sticks left.\n");
                            }
                        }
                    }
                }
            }

            else
            {
                computerMove();
                if (checkForWinner()) {
                    findWinner();
                    sc.close();
                    return;
                }
                humanTurn = true;
            }
        }
    }

    //Main method.
    //Initiates the game and then plays it.
    public static void main(String[] args)
    {
        GameOfNIM game = initiateGame();
        game.playGame();
    }

}


