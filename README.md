# Pluggit

Home Assistant integration for Pluggit ventilation units

> [!NOTE]
> This integration is based on the Dantherm integration, as Pluggit and Dantherm ventilation units appear to share the same controller hardware. To avoid maintaining the code in two separate places, most of the code in this repository is copied from the Dantherm integration with each release. For more detailed documentation, please refer to the Dantherm integration [here](https://github.com/Tvalley71/dantherm).

<a href="https://www.buymeacoffee.com/tvalley71" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

### Support

You can [open issues directly](https://github.com/Tvalley71/pluggit/issues/new) on this repository. To keep discussions centralized, please refer to the Dantherm Integration [here](https://github.com/Tvalley71/dantherm/discussions).

Known supported units:

- AP310

Please let me know if any other models are supported by clicking [here](https://github.com/Tvalley71/dantherm/discussions/new?category=general). Be sure to include both the model name and the unit type number. The unit type number can be found in the **Device Info** on the Integration page in Home Assistant, listed as "Unknown" followed by a number if the unit is not recognized by the integration.

### Installation

#### Installation via HACS (Home Assistant Community Store)

1. Ensure you have HACS installed and configured in your Home Assistant instance.
2. Open the HACS (Home Assistant Community Store) by clicking **HACS** in the side menu.
3. Click on **Integrations** and then click the **Explore & Download Repositories** button.
4. Search for "Pluggit" in the search bar.
5. Locate the "Pluggit Integration" repository and click on it.
6. Click the **Install** button.
7. Once installed, restart your Home Assistant instance.

#### Manual Installation

1. Navigate to your Home Assistant configuration directory.
    - For most installations, this will be **'/config/'**.
2. Inside the configuration directory, create a new folder named **'custom_components'** if it does not already exist.
3. Inside the **'custom_components'** folder, create a new folder named **'pluggit'**.
4. Download the latest release of the Pluggit integration from the [releases page](https://github.com/Tvalley71/pluggit/releases/latest) into the **'custom_components/pluggit'** directory:
5. Once the files are in place, restart your Home Assistant instance.

### Configuration

After installation, add the Pluggit integration to your Home Assistant configuration.

1. In Home Assistant, go to **Configuration > Integrations.**
2. Click the **+** button to add a new integration.
3. Search for "Pluggit" and select it from the list of available integrations.
4. Follow the on-screen instructions to complete the integration setup.


## Disclaimer

The trademark "Pluggit" is owned by Pluggit GmbH.

The trademark "Dantherm" is owned by Dantherm Group A/S.

All product names, trademarks, and registered trademarks mentioned in this repository are the property of their respective owners.

#### I am not affiliated with Pluggit or Dantherm, except as the owner of a Dantherm HCV400 P2 unit.

### The author does not guarantee the functionality of this integration and is not responsible for any damage.

_Tvalley71_
