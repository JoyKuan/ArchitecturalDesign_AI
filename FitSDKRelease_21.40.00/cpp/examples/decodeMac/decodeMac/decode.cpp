////////////////////////////////////////////////////////////////////////////////
// The following FIT Protocol software provided may be used with FIT protocol
// devices only and remains the copyrighted property of Garmin Canada Inc.
// The software is being provided on an "as-is" basis and as an accommodation,
// and therefore all warranties, representations, or guarantees of any kind
// (whether express, implied or statutory) including, without limitation,
// warranties of merchantability, non-infringement, or fitness for a particular
// purpose, are specifically disclaimed.
//
// Copyright 2008 Garmin Canada Inc.
////////////////////////////////////////////////////////////////////////////////

#include <fstream>
#include <iostream>

#include "fit_decode.hpp"
#include "fit_mesg_broadcaster.hpp"
#include "fit_developer_field_description.hpp"

class Listener
    : public fit::FileIdMesgListener
    , public fit::UserProfileMesgListener
    , public fit::MonitoringMesgListener
    , public fit::DeviceInfoMesgListener
    , public fit::MesgListener
    , public fit::DeveloperFieldDescriptionListener
{
public :
    static void PrintValues(const fit::FieldBase& field)
    {
        for (FIT_UINT8 j=0; j< (FIT_UINT8)field.GetNumValues(); j++)
        {
            std::wcout << L"       Val" << j << L": ";
            switch (field.GetType())
            {
            // Get float 64 values for numeric types to receive values that have
            // their scale and offset properly applied.
            case FIT_BASE_TYPE_ENUM:
            case FIT_BASE_TYPE_BYTE:
            case FIT_BASE_TYPE_SINT8:
            case FIT_BASE_TYPE_UINT8:
            case FIT_BASE_TYPE_SINT16:
            case FIT_BASE_TYPE_UINT16:
            case FIT_BASE_TYPE_SINT32:
            case FIT_BASE_TYPE_UINT32:
            case FIT_BASE_TYPE_SINT64:
            case FIT_BASE_TYPE_UINT64:
            case FIT_BASE_TYPE_UINT8Z:
            case FIT_BASE_TYPE_UINT16Z:
            case FIT_BASE_TYPE_UINT32Z:
            case FIT_BASE_TYPE_UINT64Z:
            case FIT_BASE_TYPE_FLOAT32:
            case FIT_BASE_TYPE_FLOAT64:
                std::wcout << field.GetFLOAT64Value(j);
                break;
            case FIT_BASE_TYPE_STRING:
                std::wcout << field.GetSTRINGValue(j);
                break;
            default:
                break;
            }
            std::wcout << L" " << field.GetUnits().c_str() << L"\n";;
        }
    }

    void OnMesg(fit::Mesg& mesg) override
    {
        printf("On Mesg:\n");
        std::wcout << L"   New Mesg: " << mesg.GetName().c_str() << L".  It has " << mesg.GetNumFields() << L" field(s) and " << mesg.GetNumDevFields() << " developer field(s).\n";

        for (FIT_UINT16 i = 0; i < (FIT_UINT16)mesg.GetNumFields(); i++)
        {
            fit::Field* field = mesg.GetFieldByIndex(i);
            std::wcout << L"   Field" << i << " (" << field->GetName().c_str() << ") has " << field->GetNumValues() << L" value(s)\n";
            PrintValues(*field);
        }

        for (auto devField : mesg.GetDeveloperFields())
        {
            std::wcout << L"   Developer Field(" << devField.GetName().c_str() << ") has " << devField.GetNumValues() << L" value(s)\n";
            PrintValues(devField);
        }
    }

   void OnMesg(fit::FileIdMesg& mesg) override
   {
      printf("File ID:\n");
      if (mesg.GetType() != FIT_FILE_INVALID)
         printf("   Type: %d\n", mesg.GetType());
      if (mesg.GetManufacturer() != FIT_MANUFACTURER_INVALID)
         printf("   Manufacturer: %d\n", mesg.GetManufacturer());
      if (mesg.GetProduct() != FIT_UINT16_INVALID)
         printf("   Product: %d\n", mesg.GetProduct());
      if (mesg.GetSerialNumber() != FIT_UINT32Z_INVALID)
         printf("   Serial Number: %u\n", mesg.GetSerialNumber());
      if (mesg.GetNumber() != FIT_UINT16_INVALID)
         printf("   Number: %d\n", mesg.GetNumber());
   }

   void OnMesg(fit::UserProfileMesg& mesg) override
   {
      printf("User profile:\n");
      if (mesg.GetFriendlyName() != FIT_WSTRING_INVALID)
         std::wcout << L"   Friendly Name: " << mesg.GetFriendlyName().c_str() << L"\n";
      if (mesg.GetGender() == FIT_GENDER_MALE)
         printf("   Gender: Male\n");
      if (mesg.GetGender() == FIT_GENDER_FEMALE)
         printf("   Gender: Female\n");
      if (mesg.GetAge() != FIT_UINT8_INVALID)
         printf("   Age [years]: %d\n", mesg.GetAge());
      FIT_FLOAT32 weight = mesg.GetWeight();
      FIT_FLOAT32 invFloat = FIT_FLOAT32_INVALID;
      if(memcmp(&weight, &invFloat, sizeof(FIT_FLOAT32)) != 0)
         printf("   Weight [kg]: %0.2f\n", weight);
   }

   void OnMesg(fit::DeviceInfoMesg& mesg) override
   {
      printf("Device info:\n");

      if (mesg.GetTimestamp() != FIT_UINT32_INVALID)
         printf("   Timestamp: %u\n", mesg.GetTimestamp());

      switch(mesg.GetBatteryStatus())
      {
      case FIT_BATTERY_STATUS_CRITICAL:
         printf("   Battery status: Critical\n");
         break;
      case FIT_BATTERY_STATUS_GOOD:
         printf("   Battery status: Good\n");
         break;
      case FIT_BATTERY_STATUS_LOW:
         printf("   Battery status: Low\n");
         break;
      case FIT_BATTERY_STATUS_NEW:
         printf("   Battery status: New\n");
         break;
      case FIT_BATTERY_STATUS_OK:
         printf("   Battery status: OK\n");
         break;
      default:
         printf("   Battery status: Invalid\n");
         break;
      }
   }

   void OnMesg(fit::MonitoringMesg& mesg) override
   {
      printf("Monitoring:\n");

      if (mesg.GetTimestamp() != FIT_UINT32_INVALID)
      {
         printf("   Timestamp: %u\n", mesg.GetTimestamp());
      }

      if(mesg.GetActivityType() != FIT_ACTIVITY_TYPE_INVALID)
      {
         printf("   Activity type: %d\n", mesg.GetActivityType());
      }

      switch(mesg.GetActivityType()) // The Cycling field is dynamic
      {
      case FIT_ACTIVITY_TYPE_WALKING:
      case FIT_ACTIVITY_TYPE_RUNNING: // Intentional fallthrough
         if(mesg.GetSteps() != FIT_UINT32_INVALID)
         {
            printf("   Steps: %u\n", mesg.GetSteps());
         }
         break;
      case FIT_ACTIVITY_TYPE_CYCLING:
      case FIT_ACTIVITY_TYPE_SWIMMING: // Intentional fallthrough
         if(mesg.GetStrokes() != (FIT_FLOAT32)(FIT_UINT32_INVALID/2) )
         {
            printf(   "Strokes: %f\n", mesg.GetStrokes());
         }
         break;
      default:
         if(mesg.GetCycles() != (FIT_FLOAT32)(FIT_UINT32_INVALID/2) )
         {
            printf(   "Cycles: %f\n", mesg.GetStrokes());
         }
         break;
      }
   }

   void OnDeveloperFieldDescription( const fit::DeveloperFieldDescription& desc ) override
   {
       printf( "New Developer Field Description\n" );
       printf( "   App Version: %d\n", desc.GetApplicationVersion() );
       printf( "   Field Number: %d\n", desc.GetFieldDefinitionNumber() );
   }
};

int main(int argc, char* argv[])
{
   fit::Decode decode;
   fit::MesgBroadcaster mesgBroadcaster;
   Listener listener;
   std::fstream file;

   printf("FIT Decode Example Application\n");

   if (argc != 2)
   {
      printf("Usage: decode.exe <filename>\n");
      return -1;
   }

   file.open(argv[1], std::ios::in | std::ios::binary);

   if (!file.is_open())
   {
      printf("Error opening file %s\n", argv[1]);
      return -1;
   }

   if (!decode.CheckIntegrity(file))
   {
      printf("FIT file integrity failed.\n");
      return -1;
   }

   mesgBroadcaster.AddListener((fit::FileIdMesgListener &)listener);
   mesgBroadcaster.AddListener((fit::UserProfileMesgListener &)listener);
   mesgBroadcaster.AddListener((fit::MonitoringMesgListener &)listener);
   mesgBroadcaster.AddListener((fit::DeviceInfoMesgListener &)listener);
   mesgBroadcaster.AddListener((fit::MesgListener &)listener);

   try
   {
      decode.Read(&file, &mesgBroadcaster, &mesgBroadcaster, &listener);
   }
   catch (const fit::RuntimeException& e)
   {
      printf("Exception decoding file: %s\n", e.what());
      return -1;
   }

   printf("Decoded FIT file %s.\n", argv[1]);

   return 0;
}

